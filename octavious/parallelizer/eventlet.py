from __future__ import absolute_import

import eventlet

from octavious.parallelizer import Parallelizer


class EventletParallelizer(Parallelizer):
    """A parallelizer implementation for parallelizing via green threads using
    eventlet"""

    def __init__(self, patch_builtins=True):
        """
        :param patch_builtins: Indicates whether the blocker built-ins
                               will be patched or not.
        :param type: boolean
        """
        if patch_builtins:
            eventlet.monkey_patch()

    def parallelize(self, processors, input=None, callback=None):
            """Convenient ``Parallelizer.parallelize`` implementation using `eventlet`
            library.
            """
            pool = eventlet.GreenPool()
            results = list()

            def aux(gt, *args, **kwargs):
                result = gt.wait()
                results.append(result)
                if callback:
                    callback(result)

            for processor in processors:
                greenth = pool.spawn(processor, input)
                greenth.link(aux)

            pool.waitall()

            return results


parallelizer = EventletParallelizer

