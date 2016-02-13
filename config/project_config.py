import yaml
import os


class ProjectConfig:
    def __init__(self):  # , config_yaml, samples_yaml):
        self.__config_yaml_path = "Config/project_config.yaml"
        config_stream = open(self.config_yaml_path, 'r')
        self.__config_yaml = yaml.load(config_stream)
        config_stream.close()

    @property
    def bowtie_path(self):
        return self.config_yaml["bowtie_path"]

    @property
    def config_yaml_path(self):
        return self.__config_yaml_path

    @property
    def config_yaml(self):
        return self.__config_yaml

    @property
    def samtools_path(self):
        return self.config_yaml["samtools_path"]

    @property
    def use_bowtie_2(self):
        return self.config_yaml["use_bowtie_2"]

    @property
    def bismark_path(self):
        return self.config_yaml["bismark_path"]

    @property
    def converted_genome_path(self):
        return self.config_yaml["converted_genome_path"]

    @property
    def trim_galore_path(self):
        return self.config_yaml["trim_galore_path"]

    @property
    def fastqc_path(self):
        return self.config_yaml["fastqc_path"]

    @property
    def output_alignment_dir(self):
        return self.config_yaml["output_alignment_folder"]

    @property
    def condor_logs_dir(self):
        return self.config_yaml["condor_logs_dir"]

    @property
    def samtools_dir(self):
        return self.config_yaml["samtools_dir_path"]

    @property
    def deduplicate_bismark_path(self):
        return self.config_yaml["deduplicate_bismark_path"]

    @property
    def bismark_methylation_extractor_path(self):
        return self.config_yaml["bismark_methylation_extractor_path"]

    @property
    def merged_samples_dir(self):
        return self.config_yaml["merged_samples_dir"]

    @property
    def sustools_jar_path(self):
        return self.config_yaml["sustools_jar_path"]

    @property
    def r_files_path(self):
        return self.config_yaml["r_files_path"]

    @property
    def plot_sample_distribution_path(self):
        return os.path.join(self.r_files_path, "plot_sample_info.R")

    @property
    def bamtools_path(self):
        return self.config_yaml["bamtools_path"]

    @property
    def bamtools_filter_script_path(self):
        return self.config_yaml["bamtools_filter_script_path"]
