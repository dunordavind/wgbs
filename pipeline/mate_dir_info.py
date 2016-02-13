__author__ = 'med-pvo'

import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.project_config import ProjectConfig
import shutil


class MateDirInfo:
    def __init__(self, mate):
        pcfg = ProjectConfig()
        self.__mate = mate
        self.__first = mate.first
        self.__second = mate.second
        self.__output_dir = os.path.join(pcfg.output_alignment_dir, self.mate.name)

    @property
    def mate(self):
        return self.__mate

    @property
    def first(self):
        return self.__first

    @property
    def second(self):
        return self.__second

    @property
    def output_dir(self):
        return self.__output_dir

    @property
    def first_fastqc_zip_path(self):
        file_name = os.path.basename(os.path.normpath(self.first))
        file_name = fastq_to_zip_name(file_name)
        file_path = os.path.join(self.fastqc_output_dir, file_name)
        return file_path

    @property
    def second_fastqc_zip_path(self):
        file_name = os.path.basename(os.path.normpath(self.second))
        file_name = fastq_to_zip_name(file_name)
        file_path = os.path.join(self.fastqc_output_dir, file_name)
        return file_path

    @property
    def submit_file_path(self):
        return self.path_in_output_dir("pipeline_submit_file.py")

    @property
    def aligned_bam_path(self):
        name = os.path.basename(self.first_mate_trimmed_file_path) + "_bismark_bt2_pe.bam"
        return os.path.join(self.bismark_output_dir, name)

    @property
    def deduplicated_bam_path(self):
        return re.sub(".bam", ".deduplicated.bam", self.aligned_bam_path)

    @property
    def deduplication_report_path(self):
        return re.sub("deduplicated.bam", "deduplication_report.txt", self.deduplicated_bam_path)

    @property
    def bismark_methylation_extractor_output_dir(self):
        return self.path_in_output_dir("ExtractedMethylation")

    @property
    def bismark_output_dir(self):
        return self.path_in_output_dir("BismarkAlignedFiles")

    @property
    def trim_galore_output_dir(self):
        return self.path_in_output_dir("TrimGaloreOutput")

    @property
    def first_mate_trimmed_file_path(self):
        file_name = self.file_name_from_path(self.first) + "_val_1.fq.gz"
        return os.path.join(self.trim_galore_output_dir, file_name)

    @property
    def second_mate_trimmed_file_path(self):
        file_name = self.file_name_from_path(self.second) + "_val_2.fq.gz"
        return os.path.join(self.trim_galore_output_dir, file_name)

    @property
    def fastqc_output_dir(self):
        return self.path_in_output_dir("FastqcOutput")

    @property
    def alignment_report_path(self):
        return re.sub("pe.bam", "PE_report.txt", self.aligned_bam_path)


    def file_name_from_path(self, file_path):
        file_name_with_extension = os.path.basename(file_path)
        return re.sub(".fastq.gz", "", file_name_with_extension)

    def path_in_output_dir(self, relative_path):
        return os.path.join(self.output_dir, relative_path)

    def prepare_output_dir(self, clean=True):
        #create a directory where all mate data will be stored, if not exist
        if not os.path.exists(self.output_dir):
            self.create_dirs()
        elif clean:
            shutil.rmtree(self.output_dir)
            self.create_dirs()

    def create_dirs(self):
        os.mkdir(self.output_dir)
        os.mkdir(self.fastqc_output_dir)
        os.mkdir(self.bismark_output_dir)
        os.mkdir(self.bismark_methylation_extractor_output_dir)
        os.mkdir(self.trim_galore_output_dir)



def fastq_to_zip_name(file_name):
    file_name = re.sub("\.gz", "", file_name)
    file_name = re.sub("\.", "_", file_name)
    file_name = re.sub("fastq", "fastqc", file_name)
    file_name += ".zip"
    return file_name