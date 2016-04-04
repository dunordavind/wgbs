# coding=utf-8
import argparse
import os
import re
import config.global_configs as global_configs
from config.project_config import ProjectConfig
from config.samples_config import SamplesConfig
from pipeline.condor_submitter import CondorSubmitter
from pipeline.mate_dir_info import MateDirInfo
from pipeline.mate_pipeline import MatePipeline
from pipeline.sample_dir_info import SampleDirInfo
from pipeline.sample_pipeline import SamplePipeline
from structures.mate_handler import MateHandler
from tools.bismark.bismark_report import BismarkReport
from tools.bismark.deduplicate_report import DeduplicationReportParser
from tools.count_fastq_reads import count_fastq_reads


class CommandChoices:
    list_samples = "listSamples"
    list_mates = "listMates"
    merge_sample_alignments = "mergeSampleAlignments"
    align_sample = "alignSample"
    print_sample_statistics = "sampleStatistics"
    validate_config_yaml = "validateConfig"


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Whole-Genome sequencing analysis pipeline")
    subparsers = parser.add_subparsers()
    add_list_samples(subparsers)
    add_merge_sample_alignments(subparsers)
    add_align_sample(subparsers)
    add_print_sample_statistics(subparsers)
    add_validate_config_yaml(subparsers)
    return parser.parse_args()

def add_validate_config_yaml(subparsers):
    add_validate_config_yaml_parser = subparsers.add_parser(CommandChoices.validate_config_yaml,
                                                            help="validate config yaml for a sample")
    add_validate_config_yaml_parser.add_argument('-c', '--config', help="Config yaml file with samples info")
    add_validate_config_yaml_parser.set_defaults(func=validate_config_yaml)

def add_print_sample_statistics(subparsers):
    add_print_sample_statistics_parser = subparsers.add_parser(CommandChoices.print_sample_statistics,
                                                               help="print alignment statistics for a sample")
    add_print_sample_statistics_parser.add_argument('-c',
                                                    '--config',
                                                    help="Config yaml file with samples info")
    add_print_sample_statistics_parser.add_argument('-n',
                                                    '--sampleName',
                                                    help="Name for the sample that should be aligned",
                                                    required=True)
    add_print_sample_statistics_parser.set_defaults(func=print_sample_statistics)

def add_list_samples(subparsers):
    list_samples_parser = subparsers.add_parser(CommandChoices.list_samples,
                                                help="list samples that exist in config path")
    list_samples_parser.add_argument('-c',
                                     '--config',
                                     help="Config yaml file with samples info")
    list_samples_parser.set_defaults(func=list_samples)

def add_merge_sample_alignments(subparsers):
    merge_alignments_parser = subparsers.add_parser(CommandChoices.merge_sample_alignments,
                                                help="list samples that exist in config path")
    merge_alignments_parser.add_argument('-c',
                                     '--config',
                                     help="Config yaml file with samples info",
                                     required=True)
    merge_alignments_parser.add_argument('-d',
                                     '--dependencies',
                                     help="Config yaml file with samples info",
                                     required=True)
    merge_alignments_parser.add_argument('-n',
                                     '--sampleName',
                                     help="Name for the sample that should be aligned",
                                     required=True)
    merge_alignments_parser.add_argument('-p',
                                     '--processors',
                                     type=int,
                                     help="Number of cores to submit")
    merge_alignments_parser.add_argument('-m',
                                     '--memory',
                                     type=int,
                                     help="Memory")
    merge_alignments_parser.set_defaults(func=merge_sample_alignments)

def add_align_sample(subparsers):
    align_sample_parser = subparsers.add_parser(CommandChoices.align_sample,
                                                help="align a sample with a given name")
    align_sample_parser.add_argument('-c',
                                     '--config',
                                     help="Config yaml file with samples info",
                                     required=True)
    align_sample_parser.add_argument('-d',
                                     '--dependencies',
                                     help="Config yaml file with samples info",
                                     required=True)
    align_sample_parser.add_argument('-n',
                                     '--sampleName',
                                     help="Name for the sample that should be aligned",
                                     required=True)
    align_sample_parser.add_argument('-p',
                                     '--processors',
                                     type=int,
                                     help="Number of cores to submit")
    align_sample_parser.add_argument('-m',
                                     '--memory',
                                     type=int,
                                     help="Memory")
    align_sample_parser.set_defaults(func=align_sample)

def validate_config_yaml(args):
    ##check if config exists (by reading it)
    sample_config_file_path = args.config
    mate_handler = MateHandler(sample_config_file_path)

    ##check if all files in mates exist
    messages = []
    for mate in  mate_handler.list_project_mates():
        if not os.path.isfile(mate.first):
            messages.append("File " + mate.first + " for mate " + mate.name + " does not exist")
        if not os.path.isfile(mate.second):
            messages.append("File " + mate.second + "for mate " + mate.name + " does not exist")

    for message in messages:
        print(message)

    ##check how many mates in samples there are
    for sample in mate_handler.list_samples():
        print("Sample " + sample.name + " contains " + str(len(sample.mates)) + " mates ")

    ##check if any mate files are duplicated
    seen = set()
    duplicates = []
    for mate_file in mate_handler.list_all_mate_files():
        if mate_file in seen:
            duplicates.append(mate_file)
        else:
            seen.add(mate_file)

    if len(duplicates) != 0:
        print("The following files are duplicated:")
        for duplicate in duplicates:
            print(duplicate)
    else:
        print("No duplicates found")

    ##verify naming pattern (only works for uppsala data, remove it later)
    for mate in mate_handler.list_project_mates():
        suspicious = False
        if os.path.dirname(mate.first) != os.path.dirname(mate.second):
            suspicious = True

        first_name = os.path.basename(mate.first)
        second_name = os.path.basename(mate.second)

        first_res = re.match("(.*)_R1_(.*)", first_name)
        second_res = re.match("(.*)_R2_(.*)", second_name)

        if first_res and second_res:
            if first_res.group(1) != second_res.group(1) or first_res.group(2) != second_res.group(2):
                suspicious = True
        else:
            suspicious = True

        if suspicious:
            print("This mate looks suspicious:")
            print(mate.name)
            print(mate.first)
            print(mate.second)

def list_samples(args):
    sample_config_file_path = args.config
    config = SamplesConfig(sample_config_file_path)
    for sample in config.list_sample_names():
        print(sample)

    print(config.list_sample_names())

def merge_sample_alignments(args):
    sample_config_file_path = args.config
    project_config_file_path = args.dependencies
    samples_config = SamplesConfig(sample_config_file_path)
    project_config = ProjectConfig(project_config_file_path)
    setattr(global_configs, "samples_config", samples_config)
    setattr(global_configs, "project_config", project_config)

    sample_name = args.sampleName
    mate_handler = MateHandler()
    sample = mate_handler.get_sample_by_name(sample_name)
    sp = SamplePipeline(sample)
    submitter = CondorSubmitter(sp, ncores=22, memory=220000, clean_output_dir=True)
    submitter.run_on_condor()

def align_sample(args):
    # initiate configs and insert into global config singleton
    sample_config_file_path = args.config
    project_config_file_path = args.dependencies
    samples_config = SamplesConfig(sample_config_file_path)
    project_config = ProjectConfig(project_config_file_path)
    setattr(global_configs, "samples_config", samples_config)
    setattr(global_configs, "project_config", project_config)

    sample_name = args.sampleName
    mate_handler = MateHandler()
    sample = mate_handler.get_sample_by_name(sample_name)
    for mate in sample.mates:
        pipeline = MatePipeline(mate)
        pipeline.setup()
        submitter = CondorSubmitter(pipeline, ncores=10, memory=10900)
        submitter.run_on_condor()

def print_sample_statistics(args):
    print("Counting statistics")
    sample_config_file_path = args.config
    sample_name = args.sampleName
    mate_handler = MateHandler(sample_config_file_path)
    sample = mate_handler.get_sample_by_name(sample_name)

    total_first = 0
    total_second = 0
    total_aligned = 0
    total_deduplicated = 0

    for mate in sample.mates:
        di = MateDirInfo(mate)

        total_first += count_fastq_reads(di.first_fastqc_zip_path)
        total_second += count_fastq_reads(di.second_fastqc_zip_path)

        alignment_report = BismarkReport.fromfile(di.alignment_report_path)
        total_aligned += alignment_report.num_of_aligned

        drp = DeduplicationReportParser(di.deduplication_report_path)
        total_deduplicated += drp.sequences_left()

    print("Total first: ", total_first)
    print("Total second: ", total_second)
    print("Total algined: ", total_aligned)
    print("Total deduplicated: ", total_deduplicated)


if __name__ == "__main__":
    parsed = parse_command_line_args()
    parsed.func(parsed)
