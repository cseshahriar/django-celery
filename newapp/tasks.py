import logging
# celery worker
import time
from celery import shared_task, Task
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