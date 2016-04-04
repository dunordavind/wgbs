from pipeline.mate_pipeline import MatePipeline
from pipeline.pipeline_handler import PipelineHandler
from structures.mate_handler import MateHandler


def align_sample(args):
    sample_name = args.sampleName
    mate_handler = MateHandler()
    sample = mate_handler.get_sample_by_name(sample_name)

    ## conditionally, submit all the samples directly to condor (remove in the future)
    for mate in sample.mates:
        pipeline = MatePipeline(mate)
        pipeline.setup()
        pipeline_handler = PipelineHandler(pipeline, ncores=10, memory=10900)
        pipeline_handler.run_on_condor()