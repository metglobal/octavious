from octavious.pipeline import Plugin


class DictDiggerPlugin(Plugin):

    def __init__(self, path):
        self.path = path

    def post_process(self, input, output):
        entry = output
        for component in self.path.split('.'):
            entry = entry.get(component)
        return entry

plugin = DictDiggerPlugin
