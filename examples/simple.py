import os
import sys
path = os.path.join(os.path.dirname(__file__), os.path.pardir)
sys.path.insert(0, path)

import urllib
import json
import random


from octavious.pipeline import Plugin, Pipeline
from octavious.process import Processor, MultiProcessor
from octavious.parallelizer.pcelery import CeleryParallelizer


class IOProcessor(Processor):

    def process(self, input, **kwargs):
        params = urllib.urlencode(
            {'value': random.randint(0, input['n'])})
        url = urllib.urlopen('http://httpbin.org/get?' + params)
        return url.read()


class DeserializePlugin(Plugin):

    def post_process(self, input, output):
        return json.loads(output)


class RefinePlugin(Plugin):

    def post_process(self, input, output):
        return int(output['args']['value'])


class SortPlugin(Plugin):

    def post_process(self, input, output):
        return sorted(output)

sub_pipeline = Pipeline([RefinePlugin(), DeserializePlugin()])
pipeline = Pipeline([SortPlugin()])

processors = [IOProcessor(pipeline=sub_pipeline) for i in range(20)]

multi_processor = MultiProcessor(processors,
                                 parallelizer=CeleryParallelizer(),
                                 pipeline=pipeline)

print multi_processor({'n': 100})
