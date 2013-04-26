from __future__ import absolute_import

from octavious.parallelizer import Parallelizer


class DummyParallelizer(Parallelizer):
    """This class is a dummy implementation so it runs processors one by one in
    a sequence.

    """
    def parallelize(self, processors, input=None, callback=None):
        """Convenient ``Parallelizer.parallelize`` implementation

        """
        results_list = []
        subtasks = []
        for processor in processors:
            results = processor(input)
            if callback:
                callback(results)
            results_list.append(results)
        return results_list

parallelizer = DummyParallelizer
