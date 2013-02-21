class Processor(object):
    """Base class for all processors those define a custom processing unit"""

    def process(self, input=None):
        """Abstract method expected to be implemented by subclasses those
        define a processing, calculation or io etc. behaviour

        :param input: input object
        :param type: object

        """
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        """Convenient callable implementation to provide some syntactic sugar

        """
        return self.process(*args, **kwargs)


class OneToManyProcessor(Processor):
    """Fundemental ``Processor`` implemetation which handles many
    processors to be executed using a parallelizer with one input

    """

    def __init__(self, processors, parallelizer, callback=None):
        """Constructor

        :param processors: processor list to parallelize
        :param type: list

        :param parallelizer: parallelizer instance to decorate
        :param type: ``Parallelizer``

        """
        self.processors = processors
        self.parallelizer = parallelizer
        self.callback = callback

    def process(self, input=None):
        """Implements ``process`` interface.

        :param input: input object
        :param type: object

        :returns: output
        :rtype: object

        """
        return self.parallelizer(
            self.processors, input, callback=self.callback)


class WrapperProcessor(Processor):
    """Utility ``Processor`` implemetation which handles carries a processor
    handle with its input object curried.

    """
    def __init__(self, processor, input):
        """Constructor

        :param processors: processor
        :param type: ``Processor``

        :param input: input
        :param type: object

        """
        self.processor = processor
        self.input = input

    def process(self, input=None):
        return self.processor(self.input)


class ManyToOneProcessor(Processor):
    """Fundemental ``Processor`` implemetation which handles a processor to be
    executed in parallel with many inputs

    """

    def __init__(self, processor, parallelizer, callback=None):
        """Constructor

        :param processor: processor
        :param type: ``Processor``

        :param parallelizer: parallelizer
        :param type: ``Parallelizer``

        """
        self.processor = processor
        self.parallelizer = parallelizer
        self.callback = callback

    def process(self, input=[]):
        """Implements ``process`` interface

        :param input: input object list
        :param type: list

        :returns: output
        :rtype: object

        """
        return self.parallelizer(
            [WrapperProcessor(self.processor, i) for i in input],
            callback=self.callback)


class PipelineProcessor(Processor):
    """Fundemental ``Processor`` implemetation which handles multiple
    processors to be executed through a pipeline

    """

    def __init__(self, processor, pipeline):
        """Constructor

        :param processors: processor
        :param type: list

        :param pipeline: pipeline
        :param type: ``Pipeline``

        """
        self.processor = processor
        self.pipeline = pipeline

    def process(self, input=None):
        """Implements ``process`` interface

        :param input: input object
        :param type: object

        :returns: output
        :rtype: object

        """
        return self.pipeline(self.processor, input)
