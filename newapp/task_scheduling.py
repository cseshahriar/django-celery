from datetime import timedelta
from config.celery import app
from celery.schedules import crontab

app.conf.beat_schedule = {
    'task1': {
        'task': 'newapp.task_scheduling.task1',
        'schedule': timedelta(seconds=5),
        'kwargs': {'foo': 'bar'},
        'args': (1, 2),
        'options': {
            'queue': 'tasks',
            'priory': 5,
        }
    },
    'tasks2': {
        'tasks': 'newapp.task_scheduling.task1',
        'schedule': timedelta(seconds=10),
    }
}


app.conf.beat_schedule = {
    'task3': {
        'task': 'newapp.task_schedule_crontab.task1',
        'schedule': crontab(minute='0-59/10', hour='0-5', day_of_week='mon'),
        'kwargs': {'foo': 'bar'},
        'args': (1, 2),
        'options': {
            'queue': 'tasks',
            'priory': 5,
        }
    },
}


@app.task(queue='tasks')
def tasks1(a, b, **kwargs):
    result = a + b
    print(f"Running tasks 1 - {result}")


@app.task(queue='tasks')
def tasks2():
    print("Running tasks 2")


@app.task(queue='tasks')
def tasks3(a, b, **kwargs):
    result = a + b
    print(f"Running tasks 1 - {result}")

