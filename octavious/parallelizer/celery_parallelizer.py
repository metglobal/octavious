import celery
from octavious.parallelizer import Parallelizer
from examples.dummy.tasks import function

import celery

class CeleryParallelizer(Parallelizer):	

#Works with celery and Get the processors work as a group asynchronously.
	
	def parallelize(self, processors, input=None, callback=None):
		result =  celery.group((celery.task(function)).s(processor(input)) \
								for processor in processors).apply_async()
		return result.get()
parallelizer = CeleryParallelizer
