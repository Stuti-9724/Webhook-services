import requests
import hmac
import hashlib
import json
from celery import Task
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from ..database import SessionLocal, get_redis
from .. import crud, models, schemas
from .celery_app import celery_app
import uuid

class DatabaseTask(Task):
    _db = None

    @property
    def db(self) -> Session:
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def after_return(self, *args, **kwargs):
        if self._db is not None:
            self._db.close()
            self._db = None

def generate_signature(payload: Dict[str, Any], secret_key: str) -> str:
    message = json.dumps(payload, sort_keys=True).encode()
    signature = hmac.new(secret_key.encode(), message, hashlib.sha256).hexdigest()
    return signature

@celery_app.task(base=DatabaseTask, bind=True, max_retries=5)
def deliver_webhook(self, subscription_id: int, payload: Dict[str, Any], webhook_id: Optional[str] = None) -> bool:
    if webhook_id is None:
        webhook_id = str(uuid.uuid4())

    subscription = crud.get_subscription(self.db, subscription_id)
    if not subscription:
        return False

    headers = {
        'Content-Type': 'application/json',
        'X-Webhook-ID': webhook_id
    }

    # Add signature if secret key is present
    if subscription.secret_key:
        signature = generate_signature(payload, subscription.secret_key)
        headers['X-Webhook-Signature'] = signature

    try:
        response = requests.post(
            subscription.target_url,
            json=payload,
            headers=headers,
            timeout=10  # 10 seconds timeout
        )
        response.raise_for_status()

        # Log successful delivery
        log_data = schemas.WebhookLogCreate(
            webhook_id=webhook_id,
            subscription_id=subscription_id,
            target_url=str(subscription.target_url),
            payload=payload,
            status='success',
            attempt_number=self.request.retries + 1,
            http_status=response.status_code
        )
        crud.create_webhook_log(self.db, log_data)
        return True

    except requests.RequestException as exc:
        # Log failed attempt
        log_data = schemas.WebhookLogCreate(
            webhook_id=webhook_id,
            subscription_id=subscription_id,
            target_url=str(subscription.target_url),
            payload=payload,
            status='failed',
            attempt_number=self.request.retries + 1,
            http_status=getattr(exc.response, 'status_code', None),
            error_message=str(exc)
        )
        crud.create_webhook_log(self.db, log_data)

        # Calculate retry delay with exponential backoff
        retry_delays = [10, 30, 60, 300, 900]  # 10s, 30s, 1m, 5m, 15m
        retry_delay = retry_delays[min(self.request.retries, len(retry_delays) - 1)]

        # Retry if we haven't exceeded max retries
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc, countdown=retry_delay)

        return False

@celery_app.task(base=DatabaseTask)
def cleanup_old_logs(hours: int = 72) -> None:
    crud.cleanup_old_logs(self.db, hours)