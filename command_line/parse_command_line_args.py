import argparse

from command_line.command_choises import CommandChoices
from logic.align_sample import align_sample
from logic.generate_project_makefile import generate_project_makefile
from logic.list_samples import list_samples
from logic.merge_sample_alignments import merge_sample_alignments
from logic.print_sample_statistics import print_sample_statistics
from logic.validate_config_yaml import validate_config_yaml


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Whole-Genome sequencing analysis pipeline")
    subparsers = parser.add_subparsers()
    add_list_samples(subparsers)
    add_merge_sample_alignments(subparsers)
    add_align_sample(subparsers)
    add_print_sample_statistics(subparsers)
    add_validate_config_yaml(subparsers)
    add_generate_project_makefile(subparsers)
    return parser.parse_args()


def add_generate_project_makefile(subparsers):
    add_generate_project_makefile_parser = subparsers.add_parser(CommandChoices.generate_project_makefile,
                                                                 help="generate a makefile for the whole project")
    add_generate_project_makefile_parser.add_argument('-m',
                                                      '--makefile',
                                                      help="Makefile that will run the whole project with simple make")
    add_generate_project_makefile_parser.add_argument('-c',
                                                      '--config',
                                                      help="Config yaml file with samples info",
                                                      required=True)
    add_generate_project_makefile_parser.add_argument('-d',
                                                      '--dependencies',
                                                      help="Config yaml file with the info about dependencies",
                                                      required=True)
    add_generate_project_makefile_parser.set_defaults(func=generate_project_makefile)


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
                                     help="Config yaml file with the info about dependencies",
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