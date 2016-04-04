from config import global_configs as global_configs
from pipeline.mate_pipeline import MatePipeline
from pipeline.pipeline_handler import PipelineHandler
from pipeline.sample_dir_info import SampleDirInfo
from pipeline.sample_pipeline import SamplePipeline
from structures.mate_handler import MateHandler


def generate_project_makefile(args):
    mate_handler = MateHandler()

    make_rules = [make_all_rule(mate_handler)]

    ## go through every sample and prepare a submit file path for it, as well as
    ## the path of the desired bam file
    for sample_name in global_configs.samples_config.list_sample_names()[:1]:
        ## go through every mate
        sample = mate_handler.get_sample_by_name(sample_name)

        for mate in sample.mates:
            mp = MatePipeline(mate)
            mp.setup()

            pipeline_handler = PipelineHandler(mp, ncores=10, memory=10900)
            pipeline_handler.prepare()
            make_rule = pipeline_handler.construct_align_makefile_rule()
            make_rules.append(make_rule)

        sp = SamplePipeline(sample)
        pipeline_handler = PipelineHandler(sp, ncores=22, memory=220000, clean_output_dir=True)
        pipeline_handler.prepare()
        make_rule = pipeline_handler.construct_merge_makefile_rule()
        make_rules.append(make_rule)

    for make_rule in make_rules:
        print(make_rule)
        
def make_all_rule(mate_handler):
    all_targets = [SampleDirInfo(sample).analysis_log_path for sample in mate_handler.list_samples()][:1]
    return "all : " + " ".join(all_targets) + "\n"