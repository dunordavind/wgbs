from config.project_config import ProjectConfig

__author__ = 'med-pvo'

def split_by_chromosome_command(intput_bam_file_path, output_dir ):
    config = ProjectConfig()
    command = "java -jar "
    command += config.sustools_jar_path
    command += " -i " + intput_bam_file_path + " "
    command += " -o " + output_dir + " "
    command += " -c splitByChromosome "
    return command