from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional, Dict, Any
from . import models, schemas
from datetime import datetime, timedelta
from .database import redis_client
import json

def create_subscription(db: Session, subscription: schemas.SubscriptionCreate) -> models.Subscription:
    db_subscription = models.Subscription(
        target_url=str(subscription.target_url),
        secret_key=subscription.secret_key,
        event_types=subscription.event_types
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    
    # Cache subscription data
    cache_subscription(db_subscription)
    return db_subscription

def get_subscription(db: Session, subscription_id: int) -> Optional[models.Subscription]:
    # Try to get from cache first
    cached_data = redis_client.get(f"subscription:{subscription_id}")
    if cached_data:
        return models.Subscription(**json.loads(cached_data))
    
    # If not in cache, get from database
    subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if subscription:
        cache_subscription(subscription)
    return subscription

def get_subscriptions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Subscription]:
    return db.query(models.Subscription).offset(skip).limit(limit).all()

def update_subscription(
    db: Session,
    subscription_id: int,
    subscription_update: schemas.SubscriptionUpdate
) -> Optional[models.Subscription]:
    db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if not db_subscription:
        return None

    update_data = subscription_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == 'target_url':
            setattr(db_subscription, field, str(value))
        else:
            setattr(db_subscription, field, value)

    db.commit()
    db.refresh(db_subscription)
    
    # Update cache
    cache_subscription(db_subscription)
    return db_subscription

def delete_subscription(db: Session, subscription_id: int) -> bool:
    db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if not db_subscription:
        return False

    db.delete(db_subscription)
    db.commit()
    
    # Remove from cache
    redis_client.delete(f"subscription:{subscription_id}")
    return True

def create_webhook_log(
    db: Session,
    webhook_log: schemas.WebhookLogCreate
) -> models.WebhookLog:
    db_log = models.WebhookLog(**webhook_log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_webhook_logs(
    db: Session,
    subscription_id: int,
    limit: int = 20
) -> List[models.WebhookLog]:
    return db.query(models.WebhookLog)\
        .filter(models.WebhookLog.subscription_id == subscription_id)\
        .order_by(desc(models.WebhookLog.timestamp))\
        .limit(limit)\
        .all()

def get_webhook_status(db: Session, webhook_id: str) -> Optional[Dict[str, Any]]:
    log = db.query(models.WebhookLog)\
        .filter(models.WebhookLog.webhook_id == webhook_id)\
        .order_by(desc(models.WebhookLog.timestamp))\
        .first()
    
    if not log:
        return None
        
    return {
        "webhook_id": log.webhook_id,
        "status": log.status,
        "attempts": log.attempt_number,
        "last_attempt": log.timestamp,
        "error_message": log.error_message
    }

def cleanup_old_logs(db: Session, hours: int = 72):
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    db.query(models.WebhookLog)\
        .filter(models.WebhookLog.timestamp < cutoff_time)\
        .delete()
    db.commit()

def cache_subscription(subscription: models.Subscription):
    """Cache subscription data in Redis with 10 minutes TTL"""
    subscription_data = {
        "id": subscription.id,
        "target_url": subscription.target_url,
        "secret_key": subscription.secret_key,
        "event_types": subscription.event_types,
        "created_at": subscription.created_at.isoformat(),
        "is_active": subscription.is_active
    }
    redis_client.setex(
        f"subscription:{subscription.id}",
        600,  # 10 minutes TTL
        json.dumps(subscription_data)
    )