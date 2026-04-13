#apps/notifications/email.py

from celery import shared_task
from infra_redis.stats import Stats


MESSAGE_TEXT = "Hello! This is test email from FastAPI + Celery"

@shared_task
def send_email_task(email: str):
    
    Stats.incr_sync("stats:celery:tasks_sent")
    #worker уже event-loop aware
    #можно словить RuntimeError: event loop already running
    #поэтому Stats синхронный
    print(f"Send email to {email}")
    print(MESSAGE_TEXT)
    return f"Email sent to {email}"