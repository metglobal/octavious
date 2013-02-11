from octavious.pipeline import Pipeline
from octavious.utils import pipeline, processor, plugin, parallelizer
from octavious.process import ParallelProcessor, PipelineProcessor


cnj_processor = processor('examples.simple.processes.chucknjoke')

cnj_pipeline = pipeline(
    plugin('examples.simple.plugins.echo'),
    plugin('examples.simple.plugins.dictdigger', 'value.joke'),
    plugin('examples.simple.plugins.jsondeserializer'),
)

cnj_parallelizer = parallelizer('octavious.backends.mp')

procs = [PipelineProcessor(cnj_processor, cnj_pipeline) for i in range(1, 4)]
parallel_proc = ParallelProcessor(procs, cnj_parallelizer)
parallel_proc()
