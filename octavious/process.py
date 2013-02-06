from octavious.pipeline import Pipeline


class Processor(object):
    """Base class for all processors those define a custom processing unit"""

    def __init__(self, pipeline=None):
        """Constructor

        :param pipeline: pipeline instance which gonna wrap the execution
        :param type: ``Plugin``

        """
        self.pipeline = pipeline or Pipeline([])

    def process(self, input, **kwargs):
        """Abstract method expected to be implemented by subclasses those
        define a processing, calculation or io etc. behaviour

        :param input: input object
        :param type: object

        :param **kwargs: extra keyword arguments
        :param type: dict

        """
        raise NotImplemented

    def run(self, *args, **kwargs):
        """Executes ``process`` interface by hooking it within a pipeline of
        plugins

        """
        return self.pipeline.hook(self.process, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        """Convenient callable implementation to provide some syntactic sugar

        """
        return self.run(*args, **kwargs)


class MultiProcessor(Processor):
    """Fundemental ``Processor`` implemetation which handles multiple
    processors to be executed using a pipeline within a parallelizer

    """

    def __init__(self, processors, parallelizer, pipeline=None):
        """Constructor

        :param processors: processor list to parallelize
        :param type: list

        :param parallelizer: parallelizer instance to decorate
        :param type: ``Parallelizer``

        :param pipeline: pipeline instance which gonna wrap the execution
        :param type: ``Pipeline``

        """
        super(MultiProcessor, self).__init__(pipeline=pipeline)
        self.processors = processors
        self.parallelizer = parallelizer

    def process(self, input, **kwargs):
        return self.parallelizer(self.processors, input, **kwargs)
