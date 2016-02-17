import sys
import os
import shutil
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from structures.mate_handler import MateHandler
from structures.sample import Sample
from pipeline.sample_dir_info import SampleDirInfo
from tools.samtools.samtools import samtools_merge_files_command
from tools.run_shell_command import run_shell_command
from tools.sustools.sustools import split_by_chromosome_command
from pipeline.base_pipeline import BasePipeline
from tools.bismark.bismark_methylation_extractor import BismarkMethylationExtractor
from tools.bamtools.bamtools import bamtools_clean_command

__author__ = 'med-pvo'


class SamplePipeline(BasePipeline):
    def __init__(self, sample: Sample):
        self.sample = sample
        self.__dir_info = SampleDirInfo(sample)
        self.__deduplicated = False
        self.__filtered = False
        self.log_file_handler = None

    @property
    def deduplicate(self):
        return False

    @property
    def filter(self):
        return True

    @property
    def dir_info(self):
        return self.__dir_info

    @property
    def name(self):
        name = self.sample.name
        name = re.sub("-", "_", name)
        return name

    @property
    def deduplicated(self):
        return self.__deduplicated

    @deduplicated.setter
    def deduplicated(self, value):
        self.__deduplicated = value

    @property
    def filtered(self):
        return self.__filtered

    @filtered.setter
    def filtered(self, value):
        self.__filtered = value

    def latest_processed_file(self):
        if self.filtered:
            return self.dir_info.filtered_bam_path
        elif self.deduplicated:
            return self.dir_info.deduplicated_bam_path
        else:
            return self.dir_info.aligned_bam_path

    def list_mates(self):
        return self.sample.mates

    def merge_aligned_bams(self):
        files = self.dir_info.list_aligned_bam_files()
        output_file = self.dir_info.aligned_bam_path
        if len(files) > 1:
            command = samtools_merge_files_command(output_file, files)
            print(command, file=self.log_file_handler)
            run_shell_command(command, redirect_output_path=self.dir_info.analysis_log_path, append=True)
        else:
            print("Only one bam file, skipping merging", file = self.log_file_handler)
            shutil.copyfile(files[0], output_file)

    def split_bam_by_chromosome(self):
        input_file_path = self.latest_processed_file()
        command = split_by_chromosome_command(input_file_path, self.dir_info.splitted_dir)
        print(command, file=self.log_file_handler)
        run_shell_command(command, redirect_output_path=self.dir_info.analysis_log_path, append=True)

    def extract_methylation(self):
        for file_path in os.listdir(self.dir_info.splitted_dir):
            file_path = os.path.join(self.dir_info.splitted_dir, file_path)
            extractor = BismarkMethylationExtractor(file_path,
                                                    self.dir_info.bismark_methylation_extractor_output_dir,
                                                    ncores=45)
            command = extractor.bismark_met_extractor_command()

            # perform logging
            print("*************************************", file=self.log_file_handler)
            print("This is how the extractor will be called: ", file=self.log_file_handler)
            print(command, file=self.log_file_handler)
            print("", file=self.log_file_handler)
            print("Logging extractor output to: " + extractor.log_file_path(), file=self.log_file_handler)
            print("*************************************", file=self.log_file_handler)
            print("", file=self.log_file_handler)
            print("", file=self.log_file_handler)

            # close log, because bismark likes to write to stderr and python doesnt' like it
            self.log_file_handler.close()

            # call thea actual command
            output = run_shell_command(command)

            # reopen log
            self.log_file_handler = open(self.dir_info.analysis_log_path, mode='a')
            # print(output, file=self.log_file_handler)

    def filter_quality(self):
        input_file_path = self.latest_processed_file()
        command = bamtools_clean_command(input_file_path, self.dir_info.filtered_bam_path)
        print(command, file=self.log_file_handler)
        run_shell_command(command, redirect_output_path=self.dir_info.analysis_log_path, append=True)

    def setup(self, clean_output_dir=True):
        self.dir_info.prepare_output_dir(clean=clean_output_dir)

    def pipeline(self, clean_output_dir=True):
        print("Starting")
        self.setup(clean_output_dir)
        self.log_file_handler = open(self.dir_info.analysis_log_path, mode='a')
        print("Test logging", file = self.log_file_handler)
        self.log_file_handler.close()

        # if log file already exists
        # open(self.dir_info.analysis_log_path, 'w').close()

        # setup a primitive logger (just a file handler for now)
        self.log_file_handler = open(self.dir_info.analysis_log_path, mode='a')

        print("*************************************", file=self.log_file_handler)
        print("Merging:", file=self.log_file_handler)
        self.merge_aligned_bams()
        print("*************************************", file=self.log_file_handler)
        print("", file=self.log_file_handler)
        print("", file=self.log_file_handler)

        if self.deduplicate:
            print("*************************************", file=self.log_file_handler)
            print("Deduplicating:", file=self.log_file_handler)
            self.call_deduplicate()
            self.deduplicated = True
            print("*************************************", file=self.log_file_handler)
            print("", file=self.log_file_handler)
            print("", file=self.log_file_handler)

        if self.filter:
            print("*************************************", file=self.log_file_handler)
            print("Filtering:", file=self.log_file_handler)
            self.filter_quality()
            self.filtered = True
            print("*************************************", file=self.log_file_handler)
            print("", file=self.log_file_handler)
            print("", file=self.log_file_handler)

        print("*************************************", file=self.log_file_handler)
        print("Splitting:", file=self.log_file_handler)
        self.split_bam_by_chromosome()
        print("*************************************", file=self.log_file_handler)
        print("", file=self.log_file_handler)
        print("", file=self.log_file_handler)


        print("*************************************", file=self.log_file_handler)
        print("Extracting:", file=self.log_file_handler)
        self.extract_methylation()
        print("*************************************", file=self.log_file_handler)
        print("", file=self.log_file_handler)
        print("", file=self.log_file_handler)

        # destroy the logger
        self.log_file_handler.close()


if __name__ == "__main__":
    print("Running sample pipeline for test sample")
    mate_handler = MateHandler("Config/samples_config.yaml")
    sample = mate_handler.get_sample_by_name("test_sample")
    dir_handler = SampleDirInfo(sample)
    # print(bamtools_clean_command(dir_handler.aligned_bam_path, dir_handler.filtered_bam_path))
    # dir_handler = SampleDirInfo(sample)
    # print(dir_handler.list_aligned_bam_files())
    sp = SamplePipeline(sample)
    sp.pipeline()
