# coding=utf-8
from config.samples_config import SamplesConfig
from config.project_config import ProjectConfig
from structures.mate import Mate
from pipeline.mate_pipeline import MatePipeline
from pipeline.condor_submitter import CondorSubmitter
from condor.condor_states import CondorStates
from condor.condor_log import CondorLog


__author__ = 'med-pvo'


class CondorProject():
    def __init__(self, ncores, memory):
        self.condor_logs = []
        self.__ncores = ncores
        self.__memory = memory

    @property
    def ncores(self):
        return self.__ncores

    @property
    def memory(self):
        return self.__memory

    def list_mates_to_align(self):
        cnfg = SamplesConfig("Config/samples_config.yaml")
        mates_to_align = [Mate.from_dict(mate) for mate in cnfg.list_mates()]
        mates_to_align = filter(lambda x: x.align, mates_to_align)
        return mates_to_align

    def submit(self):
        for mate in self.list_mates_to_align():
            pipeline = MatePipeline(mate)
            submitter = CondorSubmitter(pipeline, self.ncores, self.memory)
            submitter.run_on_condor()
            self.condor_logs.append(submitter.get_condor_log())

    def list_condor_logs(self):
        logs = []
        for mate in self.list_mates_to_align():
            project_config = ProjectConfig()
            logs.append(CondorLog(mate.name, project_config.condor_logs_dir))
        return logs

    def get_jobs_statistics(self):
        idle, running, hold, error, finished = 0, 0, 0, 0, 0
        condor_logs = self.list_condor_logs()
        for log in condor_logs:
            state = log.get_job_state()
            if state == CondorStates.Error:
                error += 1
            elif state == CondorStates.Finished:
                finished += 1
            elif state == CondorStates.Hold:
                hold += 1
            elif state == CondorStates.Running:
                running += 1
            elif state == CondorStates.Idle:
                idle += 1
        return idle, running, hold, error, finished

    def print_job_statistics(self):
        stats = self.get_jobs_statistics()
        for x in range(10):
            print('{0}\r'.format(x), )
        print()
        print(stats)
        print("Idle jobs " + str(stats[0]))
        print("Running jobs " + str(stats[1]))
        print("Hold jobs " + str(stats[2]))
        print("Error jobs " + str(stats[3]))
        print("Hold jobs " + str(stats[4]))






