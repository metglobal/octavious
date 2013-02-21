from octavious.pipeline import Pipeline


def load_module(module_path, symbols=()):
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
    """Initiates a callable symbol

    :param module_path: module path
    :param type: str

    :param symbol_name: name of a symbol to load
    :param type: str

    :returns: loaded symbol
    :rtype: object

    """
    symbol = load_symbol(module_path, symbol_name)
    return symbol(*args, **kwargs)


def _wrap_call_symbol(symbol_name):
    """Wraps ``call_symbol`` function by partializing the ``symbol_name``
    argument

    :param symbol_name: name of symbol
    :param type: str


    :returns: partial ``call_symbol`` reference
    :rtype: function

    """
    def aux(module_path, *args, **kwargs):
        return call_symbol(module_path, symbol_name, *args, **kwargs)
    return aux

# Helper wrappers
plugin = _wrap_call_symbol('plugin')
processor = _wrap_call_symbol('processor')
parallelizer = _wrap_call_symbol('parallelizer')


def pipeline(*args):
    """Helper function which shortcuts creating a pipeline in an easy manner

    :param args: plugins
    :param type: list

    """

    return Pipeline(args)
