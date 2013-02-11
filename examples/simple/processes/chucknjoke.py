import urllib

from octavious.processor import Processor


class ChuckNJokeProcessor(Processor):

    def process(self, input):
        return urllib.urlopen('http://api.icndb.com/jokes/random').read()

processor = ChuckNJokeProcessor
