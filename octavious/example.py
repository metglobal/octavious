import urllib
import json
import random

from pipeline import Plugin, Pipeline
from processor import Processor, MultiProcessor
from parallelizer.mp import MultiProcessingParallelizer


class IOProcessor(Processor):

    def process(self, input, **kwargs):
        params = urllib.urlencode(
            {'value': random.randint(0, input['n'])})
        url = urllib.urlopen('http://httpbin.org/get?' + params)
        return url.read()


class DeserializerPlugin(Plugin):

    def post_process(self, input, output):
        return json.loads(output)


class RefinePlugin(Plugin):

    def post_process(self, input, output):
        return int(output['args']['value'])


class SortPlugin(Plugin):

    def post_process(self, input, output):
        return sorted(output)

sub_pipeline = Pipeline([RefinePlugin(), DeserializerPlugin()])
pipeline = Pipeline([SortPlugin()])

processors = [IOProcessor(pipeline=sub_pipeline) for i in range(20)]

multi_processor = MultiProcessor(processors,
                                 parallelizer=MultiProcessingParallelizer(),
                                 pipeline=pipeline)

print multi_processor({'n': 100})
