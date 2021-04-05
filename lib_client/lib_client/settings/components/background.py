from celery.schedules import crontab

CELERY_TASK_RESULT_EXPIRES = 3600

CELERY_BEAT_SCHEDULE = {
    'sync_db_at_midnight': {
        'task': 'store.tasks.sync_db',
        'schedule': crontab(minute=0, hour=0),
    },
}
