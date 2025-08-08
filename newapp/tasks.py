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



# asynchronous tasks execution
def execute_sync():
    result = add.apply_async(args=[5, 10], kwargs={"message": "The sum is"})
    task_result = result.get()
    print("Task is running synchronously")
    print(task_result)

def execute_async():
    result = mul.apply_async(args=[5, 10], kwargs={"message": "The sum is"})
    print("Task is running asynchronously")
    print("Task ID:", result.task_id)
