import sys
import os
import shutil
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pipeline.mate_dir_info import MateDirInfo
from config.project_config import ProjectConfig

__author__ = 'med-pvo'

class SampleDirInfo:
    def     __init__(self, sample):
        config = ProjectConfig()
        self.sample = sample
        self.__output_dir = os.path.join(config.merged_samples_dir, self.sample.name)

    @property
    def output_dir(self):
        return self.__output_dir

    def list_aligned_bam_files(self):
        return [MateDirInfo(mate).deduplicated_bam_path for mate in self.sample.mates]

    @property
    def aligned_bam_path(self):
        return self.path_in_output_dir("all_mates_merged_not_deduplicated.bam")

    @property
    def deduplicated_bam_path(self):
        return self.path_in_output_dir("all_mates_merged_deduplicated.bam")

    # name regardless of deduplication. I suppose that filtering should happen after deduplication,
    # so this version of the file is final before splitting
    @property
    def filtered_bam_path(self):
        return self.path_in_output_dir("all_mates_merged_filtered.bam")

    @property
    def bismark_methylation_extractor_output_dir(self):
        return self.path_in_output_dir("ExtractedMethylation")

    @property
    def splitted_dir(self):
        return self.path_in_output_dir("SplittedByChromosome")

    @property
    def submit_file_path(self):
        return self.path_in_output_dir("condor_submit.py")

    @property
    def plots_dir(self):
        return self.path_in_output_dir("Plots")

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
        os.mkdir(self.bismark_methylation_extractor_output_dir)
        os.mkdir(self.splitted_dir)
        os.mkdir(self.plots_dir)