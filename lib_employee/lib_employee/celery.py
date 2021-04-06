import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lib_employee.settings")

from django.conf import settings  # noqa

app = Celery("lib_employee")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings", namespace='CELERY_')
app.autodiscover_tasks()
