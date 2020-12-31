from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    # Executes every day at 12:00 p.m.
    'add-every-day-at-noon': {
        'task': 'api.tasks.run_spiders',
        'schedule': crontab(hour=12),
    },
}
app.conf.timezone = 'Europe/Warsaw'

app.autodiscover_tasks()
