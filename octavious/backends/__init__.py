class Parallelizer(object):
    """Base class for handling parallel execution of processors"""

    def parallelize(self, processors, input, **kwargs):
        """Method to implement which main parallelization occurs.

        :param processors: list of processors to parallelize
        :param type: list

        :param input: input object
        :param type: object

        :param **kwargs: extra keyword arguments
        :param type: dict

        """
        raise NotImplemented

    def __call__(self, *args, **kwargs):
        """Convenient callable implementation to provide some syntactic sugar

        """
        return self.parallelize(*args, **kwargs)
