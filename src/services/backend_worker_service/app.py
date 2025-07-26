from celery import Celery
import os

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL"),
)
celery_app.autodiscover_tasks(["worker.tasks"])
