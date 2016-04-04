# coding=utf-8
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import config.global_configs as global_configs


def samtools_merge_files_command(output_file, input_file_list):
    """This function takes a directory
    and merges all *bam files in it
    into a bam file output_file
    """
    cfg = global_configs.project_config
    command = cfg.samtools_path
    command += " cat "
    command += " -o " + output_file + " "
    command += " ".join(input_file_list)
    return command

def samtools_count_command(input_file):
    cfg = global_configs.project_config
    command = cfg.samtools_path
    command += " view -c "
    command += input_file
    return command


#class IllegalFileListError(ValueError):
#    pass

