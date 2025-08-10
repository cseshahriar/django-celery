# config/celery.py

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create a Celery app instance. The name is usually the project name.
app = Celery('config')

# Load configuration from Django settings, a namespace ensures Celery-related
# settings are prefixed with CELERY_ in your settings.py file.
app.config_from_object('django.conf:settings', namespace='CELERY')

# This line is crucial for a Django project!
# It tells Celery to look for 'tasks.py' files in all your installed apps.
app.autodiscover_tasks()


app.conf.tasks_acks_late = True
app.conf.tasks_reject_on_worker_lost = True
