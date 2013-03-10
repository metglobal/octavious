import celery

@celery.task
def function(x):
	return x


