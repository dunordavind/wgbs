import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pipeline.mate_dir_info import MateDirInfo
from tools.bismark.bismark_aligner import BismarkAligner
from tools.fastqc.fastqc import call_fastqc
from structures.mate_handler import MateHandler
from tools.trim_galore.trim_galore import TrimGalore
from tools.run_shell_command import run_shell_command
from pipeline.base_pipeline import BasePipeline


__author__ = 'med-pvo'


class MatePipeline(BasePipeline):
    def __init__(self, mate, ncores=40):
        self.__mate = mate
        self.__mate_dir_info = MateDirInfo(self.mate)
        self.ncores = ncores

    @property
    def mate(self):
        return self.__mate

    @property
    def dir_info(self) -> MateDirInfo:
        return self.__mate_dir_info

    @property
    def output_dir(self):
        return self.dir_info.output_dir

    @property
    def name(self):
        name = self.mate.name
        name = re.sub("-", "_", name)
        return name

    def setup(self, clean_output_dir=True):
        self.dir_info.prepare_output_dir(clean_output_dir)

    def call_bismark(self):
        try:
            bismark = BismarkAligner(self.dir_info.first_mate_trimmed_file_path,
                                     self.dir_info.second_mate_trimmed_file_path,
                                     self.dir_info.bismark_output_dir,
                                     self.dir_info.bismark_output_dir)
            command = bismark.generate_command()
            run_shell_command(command)
        except:
            raise Exception("Couldn't use bismark for mate " + self.name() + ", please inspect the log file")

    def call_fastqc(self):
        try:
            call_fastqc(self.dir_info.first, self.dir_info.fastqc_output_dir)
            call_fastqc(self.dir_info.second, self.dir_info.fastqc_output_dir)
        except:
            raise Exception("Couldn't deduplicate for mate " + self.name() + "! Please inspect the log file")

    def call_trim_galore(self):
        try:
            trimmer = TrimGalore(self.dir_info.first,
                                 self.dir_info.second,
                                 self.dir_info.trim_galore_output_dir)
            run_shell_command(trimmer.generate_command())
        except:
            raise Exception("Couldn't trim galore for mate " + self.name() + "! Please inspect the log file")

    def pipeline(self, clean_output_dir=True):
        self.setup(clean_output_dir)
        self.call_fastqc()
        self.call_trim_galore()
        self.call_bismark()
        self.call_deduplicate()
        ##self.extract_methylation()

    def clean(self):
        raise NotImplementedError()

if __name__ == "__main__":
    handler = MateHandler()
    test_mate = handler.get_mate_by_name("S112_tag_6_GCCAAT_L003_14101")
    pipeline = MatePipeline(test_mate)
    pipeline.pipeline()

