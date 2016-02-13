__author__ = 'med-pvo'

import glob
import os
import re
from config.project_config import ProjectConfig


class BismarkAligner(object):
    def __init__(self, first_mate, second_mate, output_dir, temp_dir, log_file = None):
        self.first_mate = first_mate
        self.second_mate = second_mate
        self.output_dir = output_dir
        self.temp_dir = temp_dir
        self.log_file = log_file if log_file else os.path.join(self.output_dir, "log.txt")

    def generate_command(self):
        cfg = ProjectConfig()
        command = cfg.bismark_path
        command += " --bowtie2 " if cfg.use_bowtie_2 else " "
        command += " --path_to_bowtie " + cfg.bowtie_path
        command += " -n 1 "
        command += " -p 4 "
        command += cfg.converted_genome_path
        command += " -1 " + self.first_mate + " -2 " + self.second_mate
        command += " -o " + self.output_dir
        command += " --temp_dir " + self.temp_dir
        command += " --bam "
        command += " --samtools_path " + cfg.samtools_path
        command += " > " + self.log_file
        command += " 2>/dev/null "
        return command
