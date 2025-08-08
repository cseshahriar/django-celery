# celery worker
from celery import shared_task
import time


# synchronous task execution

@shared_task
def add(x, y, queue='celery', task_rate_limit='1/m'):
    time.sleep(3)
    return x + y


@shared_task
def mul(x, y, queue='celery:1'):
    time.sleep(3)
    return x * y


@shared_task
def div(x, y, queue='celery:2'):
    time.sleep(3)
    return x / y


@shared_task
def mod(x, y, queue='celery:3'):
    time.sleep(3)
    return x % y
