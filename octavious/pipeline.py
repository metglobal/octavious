class StopPostProcessException(Exception):
    """Exception class which is used to interrupt pipeline ``post_process``
    execution.

    """
    def __init__(self, output):
        super(StopPostProcessException, self).__init__()
        self.output = output


class Plugin(object):
    """Base class for all kind of plugins"""

    def pre_process(self, input, **kwargs):
        """Takes effect before any actual underlying action is triggered.
        If this method returns any non ``None`` value, it breaks the current
        ``pre_processing`` loop in current container pipeline.

        :param input: any input value which subjects to current context
        :param type: object

        :param **kwargs: arbitrary keyword args
        :param type: dict

        :returns: ``None`` or any convenient output value to interrupt pipeline
        :rtype: object, None

        """
        pass

    def post_process(self, input, output, **kwargs):
        """Takes effect after actual resulting action is triggered. Any
        subclass should implement this function to take effect on output by
        returning either modified or a fresh one.

        :param input: any input value which subjects to current context
        :param type: object

        :param output: output value which is passed through in the pipeline
        :param type: object

        :param **kwargs: arbitrary keyword args
        :param type: dict

        :returns: fresh or modified output value
        :rtype: object

        """
        return output

    def hook(self, callback, input, **kwargs):
        output = self.pre_process(input, **kwargs)
        if not output:
            output = callback(input, **kwargs)
        return self.post_process(input, output, **kwargs)

    def __call__(self, *args, **kwargs):
        """Convenient callable implementation to provide some syntactic sugar

        """
        return self.hook(*args, **kwargs)


class Pipeline(Plugin):
    """Fundamental ``Plugin`` implementation which consists of several
    plugins, takes control over the execution of those plugins to
    happen in order while applying a pipeline logic just like the one that
    Django Middleware infrastrcture uses.

    """
    def __init__(self, plugins, propagates_exceptions=False):
        """Constructor

        :param plugins: list of plugins
        :type plugins: list

        :param propagates_exceptions: Whether if post_process raises
        StopPostProcessException if one of child plugins throw this
        exception.
        :param type: bool

        """
        self.plugins = plugins
        self.propagates_exceptions = propagates_exceptions

    def pre_process(self, input, **kwargs):
        """Executes all inner plugins' ``pre_process`` interface in order.
        If any of them returns a non ``None`` value, it breaks the loop by
        returning that value at all.

        :param input: input value
        :param type: object

        """
        for plugin in self.plugins:
            output = plugin.pre_process(input, **kwargs)
            if output:
                return output

    def post_process(self, input, output, **kwargs):
        """Executes all inner plugins' ``post_process`` interface in order
        by chaining the output of a plugin to the next one.

        :param input: input value
        :param type: object

        :param output: output value
        :param type: object

        :returns: output
        :return type: object

        """
        for plugin in reversed(self.plugins):
            try:
                output = plugin.post_process(input, output, **kwargs)
            except StopPostProcessException as e:
                if self.propagates_exceptions:
                    raise e
                output = e.output
                break
        return output
