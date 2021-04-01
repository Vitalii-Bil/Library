import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lib_client.settings')

app = Celery('lib_client')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'sync_db_at_midnight': {
        'task': 'posts.tasks.sync_db',
        'schedule': crontab(minute=0, hour=0),
    },
}
