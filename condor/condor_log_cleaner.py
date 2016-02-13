import glob
import os
import shutil

__author__ = 'med-pvo'


class CondorLogCleaner():
    def __init__(self, prefix, directory="./"):
        self.__directory = directory  # directory where the logs are stored
        self.__prefix = prefix  # condor log prefix

    @property
    def directory(self):
        return self.__directory

    @property
    def prefix(self):
        return self.__prefix

    def clean(self):
        files = glob.glob(os.path.join(self.directory, self.prefix + "*"))
        if len(files) == 0:
            return
        else:
            [os.remove(file) for file in files]