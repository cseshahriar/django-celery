import logging

import celery
import time
import sys
from time import sleep
from celery.signals import task_failure
from celery import shared_task, Task, group, Celery
from config.celery import app

logger = logging.getLogger(__name__)


# custom tasks

class CustomTask(Task):
    ''' custom tasks '''

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if isinstance(exc, ConnectionError):
            logging.error('Connection error occurred...')
        else:
            print(f'{task_id} failed: {exc!r}')
            # Perform additional error handling actions if needed


app.Task = CustomTask

# task retry
app.task(
    queue='tasks',
    autoretry_for=(ConnectionError),
    default_retry_delay=5,
    retry_kwargs={
        'max_retries': 5
    }
)


def my_tasks():
    ''' auto retry '''
    raise ConnectionError("Connection Error Occurred...")
    return

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


@shared_task
def my_task():
    try:
        raise ConnectionError("Connection Error Occurred...")
    except ConnectionError:
        logging.error('Connection error occurred....')
        raise ConnectionError()
    except ValueError:
        # Handle value error
        logging.error('Value error occurred...')
        # Perform specific error handling actions


# task group
# jobs = group(
#     [
#         add.s(2, 1),
#         add.s(2, 2),
#         add.s(2, 3),
#     ]
# )
# result = jobs.apply_async()
# result.ready()  # have all subtasks complete?
# result.successful()  # were all subtasks successful?
# result.get()  # [3, 4, 5]
# result.complete_count()
# result.failed()

@app.task(queue='tasks')
def my_task(number):
    if number == 3:
        raise ValueError("Error Number is Invalid")
    return number * 2


def handle_result(result):
    if result.successful():
        print(f"Task Completed:{result.get()}")
    elif result.failed() and isinstance(result.result, ValueError):
        print(f"Task failed: {result.result}")
    elif result.status == 'REVOKED':
        print(f"Task was revoked: {result.id}")

def run_tasks():
    task_group = group(my_task.s(i) for i in range(5))
    result_group = task_group.apply_async()
    result_group.get(disable_sync_subtasks=False, propagate=False)

    for result in result_group:
        handle_result(result)

# time limit


@app.task(queue="tasks", time_limit=10)
def long_running_task():
    sleep(6)
    return "Task completed successfully"

@app.task(queue="tasks", bind=True)
def process_task_result(self, result):
    if result is None:
        return "Task was revoked, skipping result processing"
    else:
        return f"Task result: {result}"

def execute_task_examples():
    # Example 1: Task with a long timeout
    result = long_running_task.delay()
    try:
        task_result = result.get(timeout=40)
        print(f"Task result: {task_result}")
    except celery.exceptions.TimeoutError:
        print("Task timed out")

    print("-" * 20)

    # Example 2: Revoking a task
    task = long_running_task.delay()
    task.revoke(terminate=True)

    sleep(3) # Give Celery time to process the revocation

    sys.stdout.write(f"Task status: {task.status}\n")

    if task.status == 'REVOKED':
        # Task was revoked, process accordingly
        process_task_result.delay(None)
    else:
        process_task_result.delay(task.result)


# failed task remove


@app.task(queue="tasks")
def cleanup_failed_task(task_id, *args, **kwargs):
    sys.stdout.write(f"CLEAN UP for task_id: {task_id}\n")


@app.task(queue="tasks")
def my_task():
    raise ValueError("Task failed")


@task_failure.connect(sender=my_task)
def handle_task_failure(sender=None, task_id=None, **kwargs):
    cleanup_failed_task.delay(task_id)

def run_task():
    my_task.apply_async()
