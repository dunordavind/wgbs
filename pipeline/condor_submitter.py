__author__ = 'med-pvo'

import sys
import os
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.project_config import ProjectConfig
from tools.run_shell_command import run_shell_command
from tools.get_project_base_dir import get_project_base_dir
from condor.condor_log import CondorLog
from condor.condor_log_cleaner import CondorLogCleaner



class CondorSubmitter():
    def __init__(self, pipeline, ncores=10, memory=10000, clean_output_dir=False):
        self.__pipeline = pipeline
        self.__ncores = ncores
        self.__memory = memory
        self.__clean_output_dir=clean_output_dir

    @property
    def clean_output_dir(self):
        return self.__clean_output_dir

    @property
    def pipeline(self):
        return self.__pipeline

    @property
    def ncores(self):
        return self.__ncores

    @property
    def memory(self):
        return self.__memory

    def submit_file_path(self):
        return self.pipeline.dir_info.submit_file_path

    def pickle_pipeline(self):
        return str(pickle.dumps(self.pipeline))

    def condor_submit_file_contents(self, pickled_str):
        command = "import sys" + "\n"
        command += "import pickle" + "\n"
        command += "sys.path.append('" + get_project_base_dir() + "')" + "\n"
        #command += "from pipeline.mate_pipeline import MatePipeline" + "\n"
        command += "pipeline = pickle.loads(" + pickled_str + ")" + "\n"
        command += "print('Analyzing sample:' + pipeline.name)" + "\n"
        command += "pipeline.pipeline(False)" + "\n" # don't delete after we started!
        return command

    def write_condor_submit_file(self):
        pickled_str = self.pickle_pipeline()
        path = self.submit_file_path()
        submit_file = open(path, 'w')
        submit_file_contents = self.condor_submit_file_contents(pickled_str)
        print(submit_file_contents, file=submit_file)
        submit_file.close()

    def construct_condor_command(self):
        cfg = ProjectConfig()
        command = "csubmit.sh"
        command += " -g "
        command += " -c " + str(self.ncores)
        command += " -m " + str(self.memory)
        command += " -i " + self.pipeline.name + " "
        command += " -p " + cfg.condor_logs_dir + " "
        command += " -b python3.3 "
        command += " -a \""
        command += self.submit_file_path()
        command += "\""
        return command

    def submit_condor_command(self):
        output = run_shell_command(self.construct_condor_command())
        print(output)

    def run_on_condor(self):
        self.get_condor_cleaner().clean()
        self.pipeline.setup()
        self.write_condor_submit_file()
        self.submit_condor_command()

    def get_condor_log(self) -> CondorLog:
        return CondorLog(*self.get_condor_log_path_parameters())

    def get_condor_cleaner(self) -> CondorLogCleaner:
        return CondorLogCleaner(*self.get_condor_log_path_parameters())

    def get_condor_log_path_parameters(self):
        project_config = ProjectConfig()
        return self.pipeline.name, project_config.condor_logs_dir


if __name__ == "__main__":
    from config.samples_config import SamplesConfig
    from structures.mate import Mate
    from pipeline.mate_pipeline import MatePipeline
    from structures.mate_handler import MateHandler
    from pipeline.sample_pipeline import SamplePipeline
    #cnfg = SamplesConfig("Config/samples_config.yaml")
    #test_mate = Mate.from_dict(cnfg.get_mate_by_name("test_mate"))
    #res.call_fastqc()
    #pipeline = MatePipeline(test_mate)
    #condor_submitter = CondorSubmitter(pipeline, ncores=20)
    #condor_submitter.run_on_condor()

    mate_handler = MateHandler()
    sample = mate_handler.get_sample_by_name("33_epignome_v4")
    sp = SamplePipeline(sample)
    submitter = CondorSubmitter(sp, ncores=45, memory=450000)
    submitter.run_on_condor()