import os
import subprocess as sp


def split(s):
    try:
        s.split()
    except IOError as detail:
        print(detail)
        print("Caught file not found exception, deleting temporary dir")
        print("Unfound file is", s.input_file)
        s.delete_dir()


class Splitter:
    def __init__(self, input_file, output_dir, prefix, n=400000):
        print("Creating splitter for output dir: ", output_dir)
        self.__input_file = os.path.abspath(input_file)
        self.__prefix = prefix
        self.__output_dir = output_dir
        self.__n = n

    @property
    def prefix(self):
        return self.__prefix
        
    @property
    def input_file(self):
        return self.__input_file

    @property
    def output_dir(self):
        return self.__output_dir

    @property
    def n(self):
        return self.__n
 
    def split(self):
        input_file = self.input_file
        if not os.path.isfile(self.input_file):
            raise IOError("File '" + input_file + "' does not exist. Deleting temporary dir")

        current_dir = os.getcwd()
        os.chdir(self.output_dir)
        zcat = sp.Popen(("zcat", self.input_file), stdout=sp.PIPE)
        sp.call(["split", "-l " + str(self.n), "-d", "-a 5", "-", self.prefix], stdin=zcat.stdout)
        os.chdir(current_dir)