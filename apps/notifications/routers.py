#apps/notifications/routers.py

from fastapi import APIRouter
from pydantic import BaseModel
from apps.notifications.email import send_email_task


router = APIRouter()


class EmailRequest(BaseModel):
    email: str


@router.post("/send-email")
def send_email(req: EmailRequest):
    task = send_email_task.delay(req.email)

    return {
        "message": "Email task created",
        "task_id": task.id,
    }

