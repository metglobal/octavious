from octavious.pipeline import Plugin


class EchoPlugin(Plugin):

    def post_process(self, input, output):
        for entry in output:
            print "* %s" % entry
            print
        return output

plugin = EchoPlugin
