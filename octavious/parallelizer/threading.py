from __future__ import absolute_import
import threading
from octavious.parallelizer import Parallelizer
from Queue import Queue


def parallelizer_task(q, processor, input, callback):
    output = q.put(processor(input))
    if callback:
        callback(output)


class ThreadsParallelizer(Parallelizer):
    """
    This is implementation for python parallelizing processors using
    python's threading higher level threading interface

    """
    def parallelize(self, processors, input=None, callback=None):
        """Convenient ``Parallelizer.parallelize`` implementation
        using `threading` library.
        """
        q = Queue()
        for processor in processors:
            t = threading.Thread(target=parallelizer_task,
                                 args=(q, processor, input, callback))
            t.daemon = True
            t.start()
        return [q.get() for i in range(len(processors))]
parallelizer = ThreadsParallelizer
