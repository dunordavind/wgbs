from pipeline.pipeline_handler import PipelineHandler
from pipeline.sample_pipeline import SamplePipeline
from structures.mate_handler import MateHandler


def merge_sample_alignments(args):
    sample_name = args.sampleName
    mate_handler = MateHandler()
    sample = mate_handler.get_sample_by_name(sample_name)
    sp = SamplePipeline(sample)
    pipeline_handler = PipelineHandler(sp, ncores=22, memory=220000, clean_output_dir=True)
    pipeline_handler.run_on_condor()