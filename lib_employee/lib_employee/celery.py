import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lib_employee.settings')

app = Celery('lib_employee')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
