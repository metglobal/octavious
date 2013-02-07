import urllib

from octavious.process import Processor
from octavious.utils import create_pipeline


class ChuckNJoke(Processor):

    def process(self, id):
        return urllib.urlopen('http://api.icndb.com/jokes/random').read()

pipeline = create_pipeline([
    'examples.simple_pipeline.plugins.echoplugin'
])

pipeline(ChuckNJoke())
