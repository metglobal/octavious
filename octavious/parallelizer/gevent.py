from __future__ import absolute_import

import gevent

from octavious.parallelizer import Parallelizer


class GeventParallelizer(Parallelizer):
    """A parallelizer implementation for parallelizing via green threads using
    gevent"""

    def __init__(self, patch_builtins=True):
        """
        :param patch_builtins: Indicates whether the blocker built-ins
                               will be patched or not.
        :param type: boolean
        """
        if patch_builtins:
            from gevent import monkey
            monkey.patch_all()

    def parallelize(self, processors, input=None, callback=None):
        """Convenient ``Parallelizer.parallelize`` implementation using `gevent`
        library.
        """
        results = []
        greenlets = []

        def aux(greenlet):
            results.append(greenlet.value)
            if callback:
                callback(greenlet.value, cumulative=results)

        for processor in processors:
            greenlet = gevent.spawn(processor, input)
            greenlet.link(aux)
            greenlets.append(greenlet)

        gevent.joinall(greenlets)

        return results

parallelizer = GeventParallelizer
