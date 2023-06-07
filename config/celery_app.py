import os
from datetime import timedelta

from django.conf import settings


from celery import Celery
from celery.decorators import periodic_task

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("task_manager")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Periodic Task
@periodic_task(run_every=timedelta(seconds=30))
def every_30_seconds():
    from task_manager.tasks.views import send_reports
    print("Running Every 30 Seconds!")
    send_reports()
