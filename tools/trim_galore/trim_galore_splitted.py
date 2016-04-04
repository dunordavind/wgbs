# coding=utf-8
import re
import sys
import os
import multiprocessing as mp
import subprocess as sp
from functools import partial
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers.chunk_list import chunk_list
from config.project_config import *
import config.global_configs as global_configs

def call_trim_galore(file_pairs, output_dir):
    config = global_configs.project_config

    for file_pair in file_pairs:
        command = config.trim_galore_path
        command += " --suppress_warn"
        command += " --trim1 --paired "
        command += file_pair[0] + " " + file_pair[1]
        command += " -o " + output_dir
        sp.call([command], shell=True)


class TrimGaloreDir:
    def __init__(self, read_1_dir, read_2_dir, output_dir, ncores=20):
        self.__read_1_dir = read_1_dir
        self.__read_2_dir = read_2_dir
        
        self.__output_dir = output_dir
        self.ncores = ncores

    def read_1_dir(self):
        return self.__read_1_dir

    def read_2_dir(self):
        return self.__read_2_dir

    def output_dir(self):
        return self.__output_dir

    def trim_all(self):
        read_1_dir = self.read_1_dir()
        read_2_dir = self.read_2_dir()
        
        pair_1_files = [read_1_dir + filename for filename in sorted(os.listdir(read_1_dir))]
        pair_2_files = [read_2_dir + filename for filename in sorted(os.listdir(read_2_dir))]
  
        paired_files = list(zip(pair_1_files, pair_2_files))
        ##check files consistency
        for pair in paired_files:
            if re.search("read1(\d+)", pair[0]).group(1) != re.search("read2(\d+)", pair[1]).group(1):
                raise Exception("TrimGalore: paired files are not consistent")

        pool = mp.Pool(processes=self.ncores)
        call_trim_galore_partial = partial(call_trim_galore, output_dir=self.output_dir())
        pool.map(call_trim_galore_partial, chunk_list(paired_files, self.ncores))
        pool.close()
        pool.join()


#class TrimGalore():
#    def __init__(self):
