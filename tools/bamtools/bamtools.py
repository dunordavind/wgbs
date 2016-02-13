__author__ = 'med-pvo'

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from config.project_config import ProjectConfig
from structures.mate_handler import MateHandler
from pipeline.sample_dir_info import SampleDirInfo


def bamtools_clean_command(input_file, output_file):
    cfg = ProjectConfig()
    command = cfg.bamtools_path
    command += filter
    command += " -in " + input_file + " "
    command += " -out " + output_file + " "
    command += " -script " + cfg.bamtools_filter_script_path
    return command

if __name__ == "__main__":
    mate_handler = MateHandler()
    sample = mate_handler.get_sample_by_name("test_sample")
    dir_handler = SampleDirInfo(sample)
    print(bamtools_clean_command(dir_handler.aligned_bam_path, dir_handler.filtered_bam_path))
