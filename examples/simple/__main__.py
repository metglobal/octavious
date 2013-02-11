from octavious.pipeline import Pipeline
from octavious.utils import pipeline, processor, plugin, parallelizer
from octavious.processor import ManyToOneProcessor, PipelineProcessor


cnj_processor = processor('examples.simple.processes.chucknjoke')

cnj_pipeline = pipeline(
    plugin('examples.simple.plugins.echo'),
    plugin('examples.simple.plugins.dictdigger', 'value.joke'),
    plugin('examples.simple.plugins.jsondeserializer'),
)

cnj_parallelizer = parallelizer('octavious.parallelizer.mp')


onetomany = ManyToOneProcessor(
    PipelineProcessor(cnj_processor, cnj_pipeline), cnj_parallelizer)

onetomany(range(1, 4))
