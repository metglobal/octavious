from octavious.pipeline import Plugin, Pipeline


def load_module(module_path, symbols=[]):
    """Loads a module by given module path

    :param module_path: module path
    :param type: str

    """
    return __import__(module_path, globals(), locals(), symbols)


def load_symbol(module_path, symbol):
    """Loads a symbol dynamically from a module by given module path

    :param module_path: module path
    :param type: str

    :param symbol: name of a symbol to load
    :param type: str

    :returns: loaded symbol
    :rtype: object

    """
    module = load_module(module_path, [symbol])
    return getattr(module, symbol)


def load_plugin(module_path, symbol='plugin'):
    """Loads a plugin dynamically from a module by given module path and
    conforms if it is a ``Plugin`` instance

    :param module_path: module path
    :param type: str

    :param symbol: name of a symbol which is a plugin class
    :param type: str

    :returns: plugin class
    :rtype: class

    """
    plugin_class = load_symbol(module_path, symbol)
    if not issubclass(plugin_class, Plugin):
        raise TypeError('invalid plugin type')
    return plugin_class


def load_plugins(module_paths, symbol='plugin'):
    """Loads one more plugin classes by given list of module paths

    :param module_paths: list of module paths
    :param type: list

    :param symbol: name of a symbol which is a plugin instance
    :param type: str

    :returns: list of loaded plugin classes
    :rtype: list

    """
    return [load_plugin(mp, symbol) for mp in module_paths]


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
    return load_symbol(module_path, class_name)


def init_class(class_path, *args, **kwargs):
    """Instantiates a class with given args and kwargs parameters

    :param class_path: class path
    :param type: str

    :returns: class instance
    :rtype: object
    """
    return load_class(class_path)(*args, **kwargs)


def init_plugin(class_path, *args, **kwargs):
    """Instantiates the class by given path and checks if it conforms the
    ``Plugin`` interface

    :param class_path: plugin class path
    :param type: str

    :returns: a plugin instance
    :rtype: Plugin

    """
    plugin_class = load_class(class_path)
    plugin = plugin_class(*args, **kwargs)
    if not isinstance(plugin, Plugin):
        raise TypeError('invalid plugin type')
    return plugin


def init_plugins(class_paths, *args, **kwargs):
    """Instantiates all the given plugin classes by given path list and returns
    them as a corresponding instance list.

    :param class_paths: list of class paths
    :param type: list

    :returns: a list of instances given by class paths
    :rtype: list

    """
    return [init_plugin(class_path, *args, **kwargs)
            for class_path in class_paths]


def create_pipeline(class_paths, *args, **kwargs):
    try:
        plugins = load_plugins(class_paths)
    except:
        plugins = init_plugins(class_paths, *args, **kwargs)
    return Pipeline(plugins)


def plug(module_path, *args, **kwargs):
    """Automatically loads and instantiates a plugin class by probing the
    symbol name ```plugin`` with given args and kwargs

    :param module_path: module path
    :param type: list

    :returns: plugin instance
    :rtype: ``Plugin``

    """
    plugin_class = load_plugin(module_path)
    return plugin_class(*args, **kwargs)
