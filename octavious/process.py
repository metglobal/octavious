from octavious.pipeline import Pipeline
from octavious.utils import backend


class Processor(object):
    """Base class for all processors those define a custom processing unit"""

    def process(self, input=None):
        """Abstract method expected to be implemented by subclasses those
        define a processing, calculation or io etc. behaviour

        :param input: input object
        :param type: object

        """
        raise NotImplemented

    def __call__(self, *args, **kwargs):
        """Convenient callable implementation to provide some syntactic sugar

        """
        return self.process(*args, **kwargs)


class ParallelProcessor(Processor):
    """Fundemental ``Processor`` implemetation which handles multiple
    processors to be executed using a parallelizer

    """

    def __init__(self, processors, parallelizer):
        """Constructor

        :param processors: processor list to parallelize
        :param type: list

        :param parallelizer: parallelizer instance to decorate
        :param type: ``Parallelizer``

        """
        self.processors = processors
        if isinstance(parallelizer, str):
            self.parallelizer = backend(parallelizer)
        else:
            self.parallelizer = parallelizer

    def process(self, input=None):
        return self.parallelizer(self.processors, input)


class PipelineProcessor(Processor):
    """Fundemental ``Processor`` implemetation which handles multiple
    processors to be executed through a pipeline

    """

    def __init__(self, processor, pipeline):
        """Constructor

        :param processors: processor list to parallelize
        :param type: list

        :param parallelizer: parallelizer instance to decorate
        :param type: ``Parallelizer``

        """
        self.processor = processor
        self.pipeline = pipeline

    def process(self, input=None):
        return self.pipeline(self.processor, input)
