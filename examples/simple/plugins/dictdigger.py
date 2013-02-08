import json

from octavious.pipeline import Plugin


class DictDiggerPlugin(Plugin):

    def __init__(self, path):
        self.path = path

    def post_process(self, input, output):
        filtered_output = []
        for entry in output:
            for component in self.path.split('.'):
                entry = entry.get(component)
            filtered_output.append(entry)
        return filtered_output

plugin = DictDiggerPlugin
