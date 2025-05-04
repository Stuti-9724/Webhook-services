from typing import Optional, List, Dict, Any
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class SubscriptionBase(BaseModel):
    target_url: HttpUrl
    secret_key: Optional[str] = None
    event_types: Optional[List[str]] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    target_url: Optional[HttpUrl] = None
    secret_key: Optional[str] = None
    event_types: Optional[List[str]] = None
    is_active: Optional[bool] = None

class Subscription(SubscriptionBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class WebhookLogBase(BaseModel):
    webhook_id: str
    target_url: str
    payload: Dict[str, Any]
    status: str
    attempt_number: int
    http_status: Optional[int] = None
    error_message: Optional[str] = None

class WebhookLogCreate(WebhookLogBase):
    subscription_id: int

class WebhookLog(WebhookLogBase):
    id: int
    subscription_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class WebhookIngest(BaseModel):
    payload: Dict[str, Any]

class WebhookDeliveryStatus(BaseModel):
    webhook_id: str
    status: str
    attempts: int
    last_attempt: Optional[datetime] = None
    error_message: Optional[str] = None