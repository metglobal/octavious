from multiprocessing import Pool

from octavious.parallelizer import Parallelizer


class MultiProcessingParallelizer(Parallelizer):
    """This class is basic implementation for parallelizing processors using
    python's builtin multiprocessing api

    """
    WORKER_COUNT = 4

    def __init__(self, worker_count=None):
        """Constructor

        :param worker_count: how many worker processes will be initialized
        :param type: int

        """
        self.worker_count = worker_count or self.WORKER_COUNT

    def parallelize(self, processors, input=None, callback=None):
        """Convenient ``Parallelizer.parallelize`` implementation using `Pool`
        class

        """
        results = []

        def aux(result):
            results.append(result)
            if callback:
                callback(result, cumulative=results)
        pool = Pool(processes=self.worker_count)
        for processor in processors:
            pool.apply_async(
                processor, (input,), callback=aux)
        pool.close()
        pool.join()
        return results

parallelizer = MultiProcessingParallelizer
