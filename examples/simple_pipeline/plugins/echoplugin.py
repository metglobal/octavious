from octavious.pipeline import Plugin


class EchoPlugin(Plugin):

    def post_process(self, input, output):
        print output
        return output

plugin = EchoPlugin()
