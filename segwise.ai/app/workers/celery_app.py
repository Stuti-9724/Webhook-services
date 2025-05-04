from celery import Celery
from celery.schedules import crontab
from os import getenv

celery_app = Celery(
    'webhook_service',
    broker=getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Configure the retry policy
celery_app.conf.task_routes = {
    'app.workers.tasks.deliver_webhook': {'queue': 'webhook_delivery'}
}

celery_app.conf.task_default_retry_delay = 10  # 10 seconds
celery_app.conf.task_max_retries = 5

# Schedule periodic tasks
celery_app.conf.beat_schedule = {
    'cleanup-old-logs': {
        'task': 'app.workers.tasks.cleanup_old_logs',
        'schedule': crontab(hour='*/12'),  # Run every 12 hours
    },
}