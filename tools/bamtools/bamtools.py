# coding=utf-8
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import config.global_configs as global_configs


def bamtools_clean_command(input_file, output_file):
    cfg = global_configs.project_config
    command = cfg.bamtools_path
    command += " filter "
    command += " -in " + input_file + " "
    command += " -out " + output_file + " "
    command += " -script " + cfg.bamtools_filter_script_path
    return command
