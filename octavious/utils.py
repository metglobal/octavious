from octavious.pipeline import Plugin, Pipeline


def load_class(class_path):
    """Instantiates the class by given class path

    :param class_path: class path
    :param type: str

    :returns: a class instance, means an object
    :rtype: object

    """
    components = class_path.split('.')
    class_name = components.pop()
    module_path = '.'.join(components)
    module = __import__(module_path, globals(), locals(), [class_name])
    return getattr(module, class_name)


def init_plugin(class_path):
    """Instantiates the class path given and checks if it conforms the
    ``Plugin`` interface

    :param class_path: plugin class path
    :param type: str

    :returns: a plugin instance
    :rtype: Plugin

    """
    plugin_class = load_class(class_path)
    plugin = plugin_class()
    if not isinstance(plugin, Plugin):
        raise TypeError('invalid plugin type')
    return plugin


def init_plugins(class_paths):
    """Instantiates all the given plugin class paths and returns them as a
    corresponding instance list.

    :param class_paths: list of class paths
    :param type: list

    :returns: a list of instances given by class paths
    :rtype: list

    """
    return [init_plugin(class_path) for class_path in class_paths]


def create_pipeline(class_paths):
    """Creates a ``Pipeline`` instance using the plugins denoted by class
    paths.

    :param class_paths: list of class paths
    :param type: list

    :returns: a pipeline instance
    :rtype: Pipeline

    """
    plugins = init_plugins(class_paths)
    return Pipeline(plugins)
