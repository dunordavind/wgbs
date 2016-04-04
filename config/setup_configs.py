from config import global_configs as global_configs
from config.project_config import ProjectConfig
from config.samples_config import SamplesConfig


def setup_configs(args):
    #setup configs
    sample_config_file_path = args.config
    samples_config = SamplesConfig(sample_config_file_path)
    setattr(global_configs, "samples_config", samples_config)

    if hasattr(args, "dependencies"):
        project_config_file_path = args.dependencies
        project_config = ProjectConfig(project_config_file_path)
        setattr(global_configs, "project_config", project_config)