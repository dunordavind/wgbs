import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config.global_configs as global_configs
from structures.mate import Mate
from structures.sample import Sample
from pipeline.mate_dir_info import MateDirInfo

__author__ = 'med-pvo'


class MateHandler():
    def __init__(self):
        self.samples_config = global_configs.samples_config

    def list_project_mates(self):
        mates = self.samples_config.list_mates()
        return [Mate.from_dict(mate) for mate in mates]

    def list_samples(self):
        sample_names = self.samples_config.list_sample_names()
        samples = []
        for name in sample_names:
            mates = [Mate.from_dict(mate) for mate in self.samples_config.list_mates_for_sample(name)]
            samples.append(Sample(mates, name))
        return samples

    def get_mate_by_name(self, name):
        mate_dict = self.samples_config.get_mate_by_name(name)
        return Mate.from_dict(mate_dict)

    def get_sample_by_name(self, name):
        mates = self.samples_config.list_mates_for_sample(name)
        mates = [Mate.from_dict(mate) for mate in mates]
        sample = Sample(mates, name)
        return sample

    def list_all_mate_files(self):
        files = []
        for mate in self.list_project_mates():
            files.extend([mate.first, mate.second])
        return files


if __name__ == "__main__":
    m = MateHandler("Config/samples_config.yaml")
    sample = m.get_sample_by_name("33_epignome_v3")
    for mate in sample.mates:
        dir_info = MateDirInfo(mate)
        print(dir_info.aligned_bam_path)