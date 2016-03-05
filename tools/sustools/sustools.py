# coding=utf-8
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import config.global_configs as global_configs

__author__ = 'med-pvo'

def split_by_chromosome_command(intput_bam_file_path, output_dir ):
    config = global_configs.project_config
    command = "java -jar "
    command += config.sustools_jar_path
    command += " -i " + intput_bam_file_path + " "
    command += " -o " + output_dir + " "
    command += " -c splitByChromosome "
    return command