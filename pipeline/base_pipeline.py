import abc
from tools.bismark.deduplicate_bismark import deduplicate_bismark_command_str
from tools.run_shell_command import run_shell_command
from tools.bismark.bismark_methylation_extractor import BismarkMethylationExtractor

__author__ = 'med-pvo'


class BasePipeline(object, metaclass=abc.ABCMeta):
    pass

    @abc.abstractproperty
    def dir_info(self):
        pass

    @abc.abstractmethod
    def pipeline(self):
        pass

    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def setup(self):
        pass

    def call_deduplicate(self):
        try:
            command_str = deduplicate_bismark_command_str(self.dir_info.aligned_bam_path)
            run_shell_command(command_str)
        except:
            raise Exception("Couldn't deduplicate for mate " + self.name + "! Please inspect the log file")

    def extract_methylation(self):
        try:
            extractor = BismarkMethylationExtractor(self.dir_info.deduplicated_bam_path,
                                                    self.dir_info.bismark_methylation_extractor_output_dir)
            command = extractor.bismark_met_extractor_command()
            run_shell_command(command)
        except:
            raise Exception("Couldn't extract methylation for mate " + self.name + "! Please inspect the log file")