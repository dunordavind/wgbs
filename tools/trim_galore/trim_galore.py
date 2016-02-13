import os
import re
from config.project_config import ProjectConfig


__author__ = 'med-pvo'



class TrimGalore():
    def __init__(self, first_mate, second_mate, output_dir):
        self.first_mate = first_mate
        self.second_mate = second_mate
        self.output_dir = output_dir

    def generate_command(self):
        config = ProjectConfig()
        command = config.trim_galore_path
        command += " --suppress_warn"
        command += " --trim1 --paired "
        command += self.first_mate + " " + self.second_mate
        command += " -o " + self.output_dir
        return command
