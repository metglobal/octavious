from __future__ import absolute_import
import threading
from octavious.parallelizer import Parallelizer
from Queue import Queue


def parallelizer_task(q, processor, input, callback):
    q.put(processor(input))
    if callback:
        callback(q.put(processor(input)))


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
        threads = []
        for processor in processors:
            t = threading.Thread(target=parallelizer_task,
                                 args=(q, processor, input, callback))
            t.daemon = True
            t.start()
            threads.append(q.get())
        return threads
parallelizer = ThreadsParallelizer
