__author__ = 'med-pvo'
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from directories.temp_dir import TempDir


class ProjectTempDirsHandler:
    def __init__(self, base_path="./"):
        ##temp dirs
        self.__splitter_tempdir1 = TempDir(base_path)
        self.__splitter_tempdir2 = TempDir(base_path)
        self.__trim_galore_tempdir = TempDir(base_path)
        self.__bismark_tempdir = TempDir(base_path)

    @property
    def splitter_tempdir1_path(self):
        return self.__splitter_tempdir1.path

    @property
    def splitter_tempdir2_path(self):
        return self.__splitter_tempdir2.path

    @property
    def trim_galore_tempdir_path(self):
        return self.__trim_galore_tempdir.path

    @property
    def bismark_tempdir_path(self):
        return self.__bismark_tempdir.path

    def create_temp_dirs(self):
        print("Creating temporary directories")
        print(self.__splitter_tempdir1.path)
        self.__splitter_tempdir1.create()
        self.__splitter_tempdir2.create()
        self.__trim_galore_tempdir.create()
        self.__bismark_tempdir.create()

    def delete_temp_dirs(self):
        print("Deleting temporary directories: ")
        self.__splitter_tempdir1.delete()
        self.__splitter_tempdir2.delete()
        self.__trim_galore_tempdir.delete()
        self.__bismark_tempdir.delete()

if __name__ == "__main__":
    test_handler = ProjectTempDirsHandler()
    test_handler.create_temp_dirs()

