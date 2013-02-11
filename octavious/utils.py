from octavious.pipeline import Plugin, Pipeline
from functools import partial


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


def _wrap_call_symbol(symbol_name):
    def aux(module_path, *args, **kwargs):
        return call_symbol(module_path, symbol_name, *args, **kwargs)
    return aux

plugin = _wrap_call_symbol('plugin')
processor = _wrap_call_symbol('processor')
parallelizer = _wrap_call_symbol('parallelizer')


def pipeline(*args):
    return Pipeline(args)
