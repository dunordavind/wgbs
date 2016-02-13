__author__ = 'med-pvo'
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import re
from config.project_config import ProjectConfig


class Mate:
    def __init__(self, name, first, second, align=True, flowcell=None, library=None, lane=None):
        self.name = name
        self.first = first
        self.second = second
        self.align = align
        self.flowcell = flowcell

    @classmethod
    def from_dict(cls, d):
        if not all(key in d.keys() for key in ["name", "first", "second", "align", "flowcell"]):
            raise  Exception("Cannot create Mate class from provided dict " + str(d))
        return Mate(**d)

    def align(self):
        return self.align

    def remove_old_condor_log(self):
        cfg = ProjectConfig()
        condor_logs_dir = cfg.condor_logs_dir
        log_files = [filepath for filepath in os.listdir(condor_logs_dir)]
        mate_log_files = [log_file for log_file in log_files if re.match(self.name, log_file)]
        print("Deleting log files:")
        [print(log_file) for log_file in mate_log_files]
        [os.remove(os.path.join(cfg.condor_logs_dir, mate_log_file)) for mate_log_file in mate_log_files]


