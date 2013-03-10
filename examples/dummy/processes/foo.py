from octavious.processor import Processor


class FooProcessor(Processor):

	def process(self, input):
		print input
		return input

processor = FooProcessor