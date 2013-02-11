import urllib

from octavious.process import Processor


class ChuckNJokeProcess(Processor):

    def process(self, input):
        return urllib.urlopen('http://api.icndb.com/jokes/random').read()

processor = ChuckNJokeProcess
