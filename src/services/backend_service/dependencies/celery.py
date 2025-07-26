import os
from functools import lru_cache

from celery import Celery


@lru_cache
def get_celery_client() -> Celery:
    return Celery(
        "api-client",
        broker=os.environ["CELERY_BROKER_URL"],
    )