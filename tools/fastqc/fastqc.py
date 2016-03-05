# coding=utf-8
import os
import sys
import subprocess as sp
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import config.global_configs as global_configs

## implemented as a function for pickling
def call_fastqc(input_file, output_report_dir, ncores=6):
    cfg = global_configs.project_config
    command = cfg.fastqc_path + " "
    command += input_file + " "
    command += " -t " + str(ncores)  # use 6 threads - max available per fastqc file
    command += " -o " + output_report_dir
    command += " > " + os.path.join(output_report_dir, "fastqc_stdout.log")
    command += " 2>/dev/null "  # redirect stderr/warnings to stdout
    print(command)
    sp.call([command], shell=True)


class FastQC:
    def __init__(self, input_fastq_path, output_report_dir, ncores=6):
        self.__input_fastq_path = input_fastq_path
        self.__output_report_dir = output_report_dir
        self.ncores = ncores

    @property
    def input_fastq_path(self) -> str:
        return self.__input_fastq_path

    @property
    def output_report_dir(self) -> str:
        return self.__output_report_dir

    def fastqc(self):
        call_fastqc(self.input_fastq_path, self.output_report_dir, self.ncores)


#if __name__ == "__main__":
    #cfg = SamplesConfig("Config/samples_config.yaml")
    #mate = Mate.from_dict(cfg.get_mate_by_name("33_EpiGnome_2_CGATGT_L001_140513"))
    #fastqc = FastQC("TestData/test.fastq.gz", "TestData")
    #fastqc.fastqc()
    #test_zip_file_path = "TestData/test_fastqc.zip"
    #parser = FastQCReport(test_zip_file_path)
    #print(parser.parse())

