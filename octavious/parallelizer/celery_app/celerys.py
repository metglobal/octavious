from __future__ import absolute_import

from celery import Celery
celery = Celery('celery_app.celery',
                broker='redis://127.0.0.1:6379/0',
                backend='redis://127.0.0.1:6379/0',
                include=['celery_app.tasks'])

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    )

if __name__ == '__main__':
    celery.start()