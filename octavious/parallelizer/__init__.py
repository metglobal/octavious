class Parallelizer(object):
    """Base class for handling parallel execution of processors"""

    def parallelize(self, processors, input=None, callback=None):
        """Method to implement which main parallelization occurs.

        :param processors: list of processors to parallelize
        :param type: list

        :param input: input object
        :param type: object

        :param callback: callback function to bump results as they occur
        :param type: callable

        """
        raise NotImplemented

    def __call__(self, *args, **kwargs):
        """Convenient callable implementation to provide some syntactic sugar

        """
        return self.parallelize(*args, **kwargs)
