import urllib

from octavious.pipeline import Pipeline
from octavious.utils import plugin, backend
from octavious.process import Processor, ParallelProcessor, PipelineProcessor
from octavious.backends.mp import MultiProcessingBackend


class ChuckNJoke(Processor):

    def __init__(self, id):
        self.id = id

    def process(self, input):
        return urllib.urlopen('http://api.icndb.com/jokes/%s' % self.id).read()

pipeline = Pipeline([
    plugin('examples.simple.plugins.echo'),
    plugin('examples.simple.plugins.dictdigger', 'value.joke'),
    plugin('examples.simple.plugins.jsondeserializer'),
])


procs = [PipelineProcessor(ChuckNJoke(n), pipeline) for n in range(1, 4)]
parallel_proc = ParallelProcessor(procs, MultiProcessingBackend())

parallel_proc()
