__author__ = 'med-pvo'

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.project_config import ProjectConfig


def deduplicate_bismark_command_str(input_file_path):
    cfg = ProjectConfig()
    command = cfg.deduplicate_bismark_path
    command += " -p " + input_file_path
    command += " --bam "
    command += " --samtools_path " + cfg.samtools_dir
    command += " > " + log_path(input_file_path)
    command += " 2>/dev/null"
    return command

def log_path(input_file_path):
    return os.path.join(os.path.dirname(input_file_path), "deduplication.log")