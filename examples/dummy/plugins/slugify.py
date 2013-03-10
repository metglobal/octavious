from octavious.pipeline import Plugin

class SlugifyPlugin(Plugin):

	def pre_process(self, input):
		print __name__, 'pre_process', input
		
	def post_process(self, input, output):
		print __name__, 'pre_process', input, output
		return '-'.join(output.split())

plugin = SlugifyPlugin