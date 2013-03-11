BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_IMPORTS = ("octavious.parallelizer.celery", )
CELERY_TASK_RESULT_EXPIRES = 300
