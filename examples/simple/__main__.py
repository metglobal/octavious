import urllib

from octavious.pipeline import Pipeline
from octavious.utils import plugin, backend
from octavious.process import Processor, ParallelProcessor
from octavious.backends.mp import MultiProcessingBackend

pipeline = Pipeline([
    plugin('examples.simple.plugins.echo'),
    plugin('examples.simple.plugins.dictdigger', 'value.joke'),
    plugin('examples.simple.plugins.jsondeserializer'),
])

multiprocessing = backend('octavious.backends.mp')


class ChuckNJoke(Processor):

    def __init__(self, id):
        self.id = id

    def process(self, input):
        return urllib.urlopen('http://api.icndb.com/jokes/%s' % self.id).read()

pp = ParallelProcessor([ChuckNJoke(1), ChuckNJoke(2), ChuckNJoke(3)],
                       parallelizer=multiprocessing)
pipeline(pp)
