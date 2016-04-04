from config.samples_config import SamplesConfig


def list_samples(args):
    sample_config_file_path = args.config
    config = SamplesConfig(sample_config_file_path)
    for sample in config.list_sample_names():
        print(sample)

    print(config.list_sample_names())