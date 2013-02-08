import json

from octavious.pipeline import Plugin


class JsonDeserializerPlugin(Plugin):

    def post_process(self, input, output):
        return json.loads(output)

plugin = JsonDeserializerPlugin
