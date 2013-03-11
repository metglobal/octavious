import celery
from octavious.parallelizer import Parallelizer
from octavious.parallelizer.celery_tasks import function

class CeleryParallelizer(Parallelizer):	

#Works with celery and Get the processors work as a group asynchronously.
	
	def parallelize(self, processors, input=None, callback=None):
		result =  celery.group(function.s(processor(input)) \
								for processor in processors).apply_async()
		return result.get()
		

parallelizer = CeleryParallelizer
