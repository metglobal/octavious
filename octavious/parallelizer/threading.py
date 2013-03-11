from __future__ import absolute_import
import threading
from octavious.parallelizer import Parallelizer


def parallelizer_task(processor, input, callback):
    output = processor(input)
    if callback:
        callback(output)
    thread = threading.currentThread()
    thread.result = output


class ThreadsParallelizer(Parallelizer):
    """
    This is implementation for python parallelizing processors using
    python's threading higher level threading interface

    """
    def parallelize(self, processors, input=None, callback=None):
        """Convenient ``Parallelizer.parallelize`` implementation
        using `threading` library.
        """
        threads = []
        for processor in processors:
            t = threading.Thread(target=parallelizer_task,
                                 args=(processor, input, callback))
            threads.append(t)
            t.start()

        for th in threads:
            th.join()
        results = [th.result for th in threads]
        return results
parallelizer = ThreadsParallelizer
