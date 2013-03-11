from octavious.utils import pipeline, processor, plugin, parallelizer
from octavious.processor import ManyToOneProcessor, PipelineProcessor


if __name__ == '__main__':

    foo_processor = processor('examples.dummy.processes.foo')

    foo_pipeline = pipeline(plugin('examples.dummy.plugins.lower'),
                            plugin('examples.dummy.plugins.slugify'))
    #CHOOSE THE PARALLELYZER THAT YOU WANT YOU USE // DJANGO MULTIPROCESSOR OR CELERY

    celery_parallelizer = parallelizer('octavious.parallelizer.celery_parallelizer')
    #celery_parallelizer = parallelizer('octavious.parallelizer.mp')

    manytoone = ManyToOneProcessor(PipelineProcessor(foo_processor,
                                                     foo_pipeline),
                                   celery_parallelizer)

    manytoone(['Hello World', 'World', 'Howdy', 'You'])
