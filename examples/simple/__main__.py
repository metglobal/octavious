import sys

from octavious.utils import pipeline, processor, plugin, parallelizer
from octavious.processor import ManyToOneProcessor, PipelineProcessor


if __name__ == '__main__':

    driver = len(sys.argv) > 1 and sys.argv[1] or 'multiprocessing'

    cnj_processor = processor('examples.simple.processes.chucknjoke')

    cnj_pipeline = pipeline(
        plugin('examples.simple.plugins.dictdigger', 'value.joke'),
        plugin('examples.simple.plugins.jsondeserializer'))

    cnj_parallelizer = parallelizer('octavious.parallelizer.%s' % driver)

    manytoone = ManyToOneProcessor(PipelineProcessor(cnj_processor,
                                                     cnj_pipeline),
                                   cnj_parallelizer)

    for result in manytoone(range(1, 4)):
        print '*', result
