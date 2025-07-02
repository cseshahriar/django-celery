# config/celery.py

import os
from celery import Celery

# Set the default Django settings module for 'celery' program
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # Adjust to your project name

# Create Celery app instance
app = Celery("django_celery")

# Load settings from Django settings.py using CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks from installed apps
app.autodiscover_tasks()
