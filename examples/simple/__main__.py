import urllib

from octavious.pipeline import Pipeline
from octavious.process import Processor
from octavious.utils import init_plugin as p


class ChuckNJoke(Processor):

    def process(self, input):
        return urllib.urlopen('http://api.icndb.com/jokes/random').read()

pipeline = Pipeline([
    p('examples.simple.plugins.echoplugin.EchoPlugin'),
    p('examples.simple.plugins.dictdigger.DictDiggerPlugin', 'value.joke'),
    p('examples.simple.plugins.jsondeserializer.JsonDeserializerPlugin'),
])

pipeline(ChuckNJoke())
