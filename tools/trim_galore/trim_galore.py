import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import config.global_configs as global_configs

class TrimGalore():
    def __init__(self, first_mate, second_mate, output_dir):
        self.first_mate = first_mate
        self.second_mate = second_mate
        self.output_dir = output_dir

    def generate_command(self):
        config = global_configs.project_config
        command = config.trim_galore_path
        command += " --suppress_warn"
        command += " --trim1 --paired "
        command += self.first_mate + " " + self.second_mate
        command += " -o " + self.output_dir
        return command
