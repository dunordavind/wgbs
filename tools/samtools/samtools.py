import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from config.project_config import ProjectConfig


def samtools_merge_files_command(output_file, input_file_list):
    """This function takes a directory
    and merges all *bam files in it
    into a bam file output_file
    """
    cfg = ProjectConfig()
    command = cfg.samtools_path
    command += " cat "
    command += " -o " + output_file + " "
    command += " ".join(input_file_list)
    return command

def samtools_count_command(input_file):
    cfg = ProjectConfig()
    command = cfg.samtools_path
    command += " view -c "
    command += input_file
    return command


class IllegalFileListError(ValueError):
    pass

