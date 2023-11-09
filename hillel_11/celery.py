import os
import time

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hillel_11.settings")

app = Celery("proj")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "add-every-midnight": {
        "task": "exchange.tasks.pull_rate",
        "schedule": crontab(minute="0", hour="0"),
    },
}


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3.0, debug_task, name="add every 5")


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"request{self.request!r}")
    print(f"Current time stamp ", (time.time()))
