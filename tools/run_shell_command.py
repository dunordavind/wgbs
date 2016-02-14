import subprocess as sp

__author__ = 'med-pvo'


def run_shell_command(command_str, redirect_output_path=None, append=False):

    # redirect standard output of the command to the provided log file
    if not (redirect_output_path is None):

        # choose whether to append to the old log or to overwrite
        if append:
            command_str += " >> "
        else:
            command_str += " > "
        command_str = command_str + redirect_output_path

    return sp.check_output([command_str], shell=True)
