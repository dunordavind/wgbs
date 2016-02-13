__author__ = 'med-pvo'
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.project_config import ProjectConfig
from tools.run_shell_command import run_shell_command

def plot_sample_distributions(input_dir, output_dir):
    config = ProjectConfig()
    command = "Rscript "
    command += config.plot_sample_distribution_path + " "
    command += input_dir + " "
    command += output_dir + " "
    print(command)
    run_shell_command(command)
