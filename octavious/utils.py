from octavious.pipeline import Plugin, Pipeline


def load_module(module_path, symbols=[]):
    """Loads a module by given module path

    :param module_path: module path
    :param type: str

    """
    return __import__(module_path, globals(), locals(), symbols)


def load_symbol(module_path, symbol_name):
    """Loads a symbol dynamically from a module by given module path

    :param module_path: module path
    :param type: str

    :param symbol_name: name of a symbol to load
    :param type: str

    :returns: loaded symbol
    :rtype: object

    """
    try:
        module = load_module(module_path, [symbol_name])
        return getattr(module, symbol_name)
    except (ImportError, AttributeError), e:
        raise ImportError(e)


def call_symbol(module_path, symbol_name, *args, **kwargs):
    symbol = load_symbol(module_path, symbol_name)
    return symbol(*args, **kwargs)


def plugin(module_path, *args, **kwargs):
    """Automatically loads and instantiates a plugin class by probing the
    symbol name ```plugin`` with given args and kwargs

    :param module_path: module path
    :param type: str

    :returns: plugin instance
    :rtype: ``Plugin``

    """
    return call_symbol(module_path, 'plugin', *args, **kwargs)


def backend(module_path, *args, **kwargs):
    """Automatically loads and instantiates a backend class by probing the
    symbol name ```backend`` with given args and kwargs

    :param module_path: module path
    :param type: str

    :returns: backend instance
    :rtype: ``Parallelizer``

    """
    return call_symbol(module_path, 'backend', *args, **kwargs)
