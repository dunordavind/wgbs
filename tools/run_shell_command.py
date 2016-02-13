__author__ = 'med-pvo'

import subprocess as sp


def run_shell_command(command_str):
    return sp.check_output([command_str], shell=True)