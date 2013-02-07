import urllib

from octavious.pipeline import Pipeline
from octavious.utils import plug
from octavious.process import Processor

pipeline = Pipeline([
    plug('examples.simple.plugins.echo'),
    plug('examples.simple.plugins.dictdigger', 'value.joke'),
    plug('examples.simple.plugins.jsondeserializer'),
])


class ChuckNJoke(Processor):

    def process(self, input):
        return urllib.urlopen('http://api.icndb.com/jokes/random').read()

pipeline(ChuckNJoke())
