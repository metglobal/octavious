from __future__ import absolute_import

import celery

from octavious.parallelizer import Parallelizer


@celery.task('parallelizer_task')
def parallelizer_task(processor, input, callback):
    output = processor(input)
    if callback:
        callback(output)
    return output


class CeleryParallelizer(Parallelizer):
    """This class is basic implementation for parallelizing processors using
    a messaging queue server through celery libraries.

    """
    def parallelize(self, processors, input=None, callback=None):
        """Convenient ``Parallelizer.parallelize`` implementation to establish
        concurrency using celery tasks

        """
        subtasks = []
        for processor in processors:
            subtasks.append(parallelizer_task.s(processor, input, callback))
        async_result = celery.group(subtasks).apply_async()
        return async_result.get()

parallelizer = CeleryParallelizer
