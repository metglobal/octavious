from octavious.pipeline import Plugin

class LowerPlugin(Plugin):

	def pre_process(self, input):
		#print __name__, 'pre_process', input
		pass
	def post_process(self, input, output):
		#print __name__, 'pre_process', input, output
		return output.lower()

plugin = LowerPlugin