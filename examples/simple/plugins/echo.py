from octavious.pipeline import Plugin


class EchoPlugin(Plugin):

    def post_process(self, input, output):
        print "* %s" % output
        print
        return output

plugin = EchoPlugin
