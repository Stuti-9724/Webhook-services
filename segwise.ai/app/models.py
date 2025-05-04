from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String, nullable=False)
    secret_key = Column(String, nullable=True)
    event_types = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationship with WebhookLog
    logs = relationship("WebhookLog", back_populates="subscription")

class WebhookLog(Base):
    __tablename__ = "webhook_logs"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    webhook_id = Column(String, index=True)
    target_url = Column(String)
    payload = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    attempt_number = Column(Integer, default=1)
    status = Column(String)  # success, failed, pending
    http_status = Column(Integer, nullable=True)
    error_message = Column(String, nullable=True)

    # Relationship with Subscription
    subscription = relationship("Subscription", back_populates="logs")