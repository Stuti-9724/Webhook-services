from fastapi import FastAPI, HTTPException, Depends, Header, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, models, schemas
from .database import engine, get_db
from .workers.tasks import deliver_webhook
from .middleware import setup_cors
import uuid

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Webhook Delivery Service",
    description="A service for managing webhook subscriptions and delivering webhook events",
    version="1.0.0"
)

# Setup CORS middleware
setup_cors(app)

@app.post("/subscriptions/", response_model=schemas.Subscription)
def create_subscription(
    subscription: schemas.SubscriptionCreate,
    db: Session = Depends(get_db)
):
    return crud.create_subscription(db=db, subscription=subscription)

@app.get("/subscriptions/{subscription_id}", response_model=schemas.Subscription)
def read_subscription(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = crud.get_subscription(db, subscription_id=subscription_id)
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription

@app.get("/subscriptions/", response_model=List[schemas.Subscription])
def list_subscriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    subscriptions = crud.get_subscriptions(db, skip=skip, limit=limit)
    return subscriptions

@app.put("/subscriptions/{subscription_id}", response_model=schemas.Subscription)
def update_subscription(
    subscription_id: int,
    subscription: schemas.SubscriptionUpdate,
    db: Session = Depends(get_db)
):
    db_subscription = crud.update_subscription(db, subscription_id, subscription)
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription

@app.delete("/subscriptions/{subscription_id}")
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    success = crud.delete_subscription(db, subscription_id=subscription_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return {"status": "success", "message": "Subscription deleted"}

@app.post("/ingest/{subscription_id}")
async def ingest_webhook(
    subscription_id: int,
    webhook_data: schemas.WebhookIngest,
    x_event_type: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    # Verify subscription exists
    subscription = crud.get_subscription(db, subscription_id=subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Check if subscription is active
    if not subscription.is_active:
        raise HTTPException(status_code=400, detail="Subscription is inactive")

    # Verify event type if subscription has event_types filter
    if subscription.event_types and x_event_type:
        if x_event_type not in subscription.event_types:
            raise HTTPException(
                status_code=400,
                detail=f"Event type {x_event_type} not allowed for this subscription"
            )

    # Generate webhook ID
    webhook_id = str(uuid.uuid4())

    # Queue webhook delivery task
    deliver_webhook.delay(
        subscription_id=subscription_id,
        payload=webhook_data.payload,
        webhook_id=webhook_id
    )

    return {
        "status": "accepted",
        "webhook_id": webhook_id,
        "message": "Webhook queued for delivery"
    }

@app.get("/status/{webhook_id}", response_model=schemas.WebhookDeliveryStatus)
def get_webhook_status(webhook_id: str, db: Session = Depends(get_db)):
    status = crud.get_webhook_status(db, webhook_id)
    if not status:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return status

@app.get("/subscriptions/{subscription_id}/logs", response_model=List[schemas.WebhookLog])
def get_subscription_logs(
    subscription_id: int,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    subscription = crud.get_subscription(db, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    logs = crud.get_webhook_logs(db, subscription_id, limit)
    return logs
    status = crud.get_webhook_status(db, webhook_id=webhook_id)
    if not status:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return status

@app.get("/subscriptions/{subscription_id}/logs", response_model=List[schemas.WebhookLog])
def get_subscription_logs(
    subscription_id: int,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    # Verify subscription exists
    subscription = crud.get_subscription(db, subscription_id=subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    return crud.get_webhook_logs(db, subscription_id=subscription_id, limit=limit)