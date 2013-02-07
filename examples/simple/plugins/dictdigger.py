import json

from octavious.pipeline import Plugin


class DictDiggerPlugin(Plugin):

    def __init__(self, path):
        self.path = path

    def post_process(self, input, output):
        for component in self.path.split('.'):
            output = output.get(component)
        return output
