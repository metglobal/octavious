import json

from octavious.pipeline import Plugin


class JsonDeserializerPlugin(Plugin):

    def post_process(self, input, output):
        filtered_output = []
        for entry in output:
            filtered_output.append(json.loads(entry))
        return filtered_output

plugin = JsonDeserializerPlugin
