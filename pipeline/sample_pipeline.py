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




__author__ = 'med-pvo'


class SamplePipeline(BasePipeline):
    def __init__(self, sample: Sample):
        self.sample = sample
        self.__dir_info = SampleDirInfo(sample)

    @property
    def dir_info(self):
        return self.__dir_info

    @property
    def name(self):
        name = self.sample.name
        name = re.sub("-", "_", name)
        return name

    def list_mates(self):
        return self.sample.mates

    def merge_aligned_bams(self):
        files = self.dir_info.list_aligned_bam_files()
        output_file = self.dir_info.aligned_bam_path
        if len(files) > 1:
            command = samtools_merge_files_command(output_file, files)
            run_shell_command(command)
        else:
            shutil.copyfile(files[0], output_file)

    def split_bam_by_chromosome(self):
        command = split_by_chromosome_command(self.dir_info.aligned_bam_path, self.dir_info.splitted_dir)
        run_shell_command(command)

    def extract_methylation(self):
        for file_path in os.listdir(self.dir_info.splitted_dir):
            file_path = os.path.join(self.dir_info.splitted_dir, file_path)
            extractor = BismarkMethylationExtractor(file_path,
                                                    self.dir_info.bismark_methylation_extractor_output_dir,
                                                    ncores=45)
            command = extractor.bismark_met_extractor_command()
            print(command)
            output = run_shell_command("time " + command)
            print(output)

    def setup(self, clean_output_dir=True):
        self.dir_info.prepare_output_dir(clean=clean_output_dir)

    def pipeline(self, clean_output_dir=True):
        self.setup(clean_output_dir)
        self.merge_aligned_bams()
        # self.call_deduplicate() # probably uncomment in the future runs
        self.split_bam_by_chromosome()
        self.extract_methylation()


if __name__ == "__main__":
    mate_handler = MateHandler()
    sample = mate_handler.get_sample_by_name("112_epignome")
    # dir_handler = SampleDirInfo(sample)
    # print(dir_handler.list_aligned_bam_files())
    sp = SamplePipeline(sample)
    sp.pipeline()
