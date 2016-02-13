from condor.condor_states import CondorStates

__author__ = 'med-pvo'

import os
import glob
import unittest
import re


class CondorLog():
    def __init__(self, prefix, directory="./"):
        self.__directory = directory  # directory where the logs are stored
        self.__prefix = prefix  # condor log prefix

    @property
    def directory(self):
        return self.__directory

    @property
    def prefix(self):
        return self.__prefix

    @property
    def log_file_path(self):
        files = glob.glob(os.path.join(self.directory, self.prefix + "*log"))
        if len(files) > 1:
            raise Exception("Log files for " + self.prefix + " are not unique! Aborting...")
        return os.path.abspath(files[0])

    @property
    def error_file_path(self):
        files = glob.glob(os.path.join(self.directory, self.prefix + "*log"))
        if len(files) > 1:
            raise Exception("Error files for " + self.prefix + " are not unique! Aborting...")
        return os.path.abspath(files[0])

    @property
    def out_file_path(self):
        files = glob.glob(os.path.join(self.directory, self.prefix + "*log"))
        if len(files) > 1:
            raise Exception("Out files for " + self.prefix + " are not unique! Aborting...")
        return os.path.abspath(files[0])

    def get_job_state(self):
        log_file = open(self.log_file_path, 'r')
        log = [line.rstrip() for line in log_file]

        ## check if idle
        if len(log) == 2 and log[1] == "...":
            log_file.close()
            return CondorStates.Idle

        ## check if error
        if any([re.search("Normal termination \(return value 1\)", line) for line in log]):
            log_file.close()
            return CondorStates.Error

        ## check if hold

        ## check if finished
        if any([re.search("Normal termination \(return value 0\)", line) for line in log]):
            log_file.close()
            return CondorStates.Finished

        ## otherwise, consider the job running
        log_file.close()
        return CondorStates.Running


if __name__ == "__main__":
    unittest.main()
