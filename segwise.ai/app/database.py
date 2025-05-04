from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from redis import Redis
from os import getenv

# Database configuration
DATABASE_URL = getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/webhook_service")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Redis configuration
REDIS_URL = getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get Redis client
def get_redis():
    return redis_client