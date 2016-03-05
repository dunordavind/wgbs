import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import config.global_configs as global_configs
import re
import multiprocessing as mp
import subprocess as sp
from functools import partial

from helpers.chunk_list import chunk_list
from config.project_config import ProjectConfig


def call_bismark(file_pairs, output_dir, temp_dir):
    cfg = global_configs.project_config
    for file_pair in file_pairs:
        command = cfg.bismark_path
        command += " --bowtie2 " if cfg.use_bowtie_2 else " "
        command += " --path_to_bowtie " + cfg.bowtie_path
        command += " -n 1 "
        command += cfg.converted_genome_path
        command += " -1 " + file_pair[0] + " -2 " + file_pair[1]
        command += " -o " + output_dir
        command += " --temp_dir " + temp_dir
        command += " --bam "
        command += " --samtools_path " + cfg.samtools_path
        command += " >/dev/null "
        sp.call([command], shell=True)


class Bismark:
    """This class takes a dir with many preprocessed mate fastq files
    in format read10000_val_1.fq and read2000_val_2.fq (this files are
    provided with trim_galore class) and applies Bismark aligner to all
    of them. In order to merge results, Samtools class and BismarkReport class should be used.
    Also, this class have no mechanisms to delete it's output dir, it should be
    handled from outside using TempDir class.
    """
    def __init__(self, trimmed_dir, output_dir, temp_dir=None, ncores=20):
        self.__trimmed_dir = trimmed_dir
        self.__output_dir = output_dir
        self.ncores = ncores
        if not temp_dir:
            self.temp_dir = output_dir
        else:
            self.temp_dir = temp_dir

    @property
    def output_dir(self):
        return self.__output_dir

    @property
    def trimmed_dir(self):
        return self.__trimmed_dir

    def call_bismark(self):
        print("Calling bismark for directory: ")
        print(self.trimmed_dir)
        all_files = os.listdir(self.trimmed_dir)

        read_1_files_re = re.compile('read1(\d+)_.*\.fq')
        read_2_files_re = re.compile('read2(\d+)_.*\.fq')

        read_1_files = [os.path.join(self.trimmed_dir, name) for name in all_files if read_1_files_re.match(name)]
        read_2_files = [os.path.join(self.trimmed_dir, name) for name in all_files if read_2_files_re.match(name)]
        paired_files = list(zip(sorted(read_1_files), sorted(read_2_files)))

        print("Paired files for bismark are: ")
        print(paired_files)

        ##check files consistency 
        for pair in paired_files:
            if read_1_files_re.search(pair[0]).group(1) != read_2_files_re.search(pair[1]).group(1):
                print(pair)
                raise Exception("Files are probably not mates!!")

        pool = mp.Pool(processes=self.ncores)
        call_bismark_partial = partial(call_bismark, output_dir=self.output_dir, temp_dir=self.temp_dir)
        pool.map(call_bismark_partial, chunk_list(paired_files, self.ncores))
        pool.close()
        pool.join()

    def clean(self):
        raise NotImplementedError("Clean not implemented")


if __name__ == "__main__":
    #trimmed_dir = "666666259c74a5-a900-488e-a6d7-aa90c17c065f"
    #genome_dir = "Genome_Info/UCSC_HG_38_main_build/chroms"
    #b = Bismark(trimmed_dir, "Test", genome_dir, ncores=10)
    #b.call_bismark()
    print("Testing")
