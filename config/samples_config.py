__author__ = 'med-pvo'

import yaml
import itertools


class SamplesConfig:
    def __init__(self, config_file_path):
        """
        This class parses SampleConfig yaml file. It allows to read an array of mates, which is
        itself a dictionary. For more details look into Config/samples_config.yaml
        :param config_file_path:
        """
        self.__samples_yaml_path = config_file_path
        samples_stream = open(self.samples_yaml_path, 'r')
        self.__samples_yaml = yaml.load(samples_stream)
        samples_stream.close()

        ##verify that mate names are unique
        if not len(self.list_mate_names()) == len(set(self.list_mate_names())):
            raise Exception("Mate names are required to be unique")

    @classmethod
    def default(cls):
        return SamplesConfig("Config/samples_config.yaml")

    @property
    def samples_yaml_path(self):
        return self.__samples_yaml_path

    @property
    def samples_yaml(self):
        return self.__samples_yaml

    def list_samples(self):
        return self.samples_yaml["data"]["samples"]

    def list_sample_names(self):
        return [sample["sample_name"] for sample in self.list_samples()]

    def list_mate_names(self):
        return [mate["name"] for mate in self.list_mates()]

    def get_sample_by_name(self, name):
        sample_names = self.list_sample_names()
        if name in sample_names:
            samples = self.list_samples()
            return samples[sample_names.index(name)]
        else:
            return None

    def list_mates(self):
        mates = [sample["mates"] for sample in self.list_samples()]
        return list(itertools.chain(*mates))

    def list_mates_for_sample(self, sample_name):
        return self.get_sample_by_name(sample_name)["mates"]

    def list_flowcell_names(self):
        return set([mate["flowcell"] for mate in self.list_mates()])

    def list_flowcell_names_for_sample(self, sample_name):
        return set([mate["flowcell"] for mate in self.list_mates_for_sample(sample_name)])

    def get_mate_by_name(self, mate_name):
        mates_with_name = [mate for mate in self.list_mates() if mate["name"] == mate_name]
        if len(mates_with_name) == 0:
            raise Exception("There is no mate with name: " + mate_name)

        if len(mates_with_name) != 1:
            for mate in mates_with_name:
                print(mate)
            raise Exception("More then one mate with given name: " + mate_name)

        mate_dict = mates_with_name[0]
        return mate_dict
