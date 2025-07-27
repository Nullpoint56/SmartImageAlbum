import os

from celery import Celery


def get_celery_client() -> Celery:
    return Celery(
        "api-client",
        broker=os.environ["CELERY_BROKER_URL"],
    )