import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from structures.mate_handler import MateHandler
from pipeline.mate_dir_info import MateDirInfo
from tools.fastqc.fastqc_summary import PairedFastqcSummary
from tools.fastqc.fastqc_tags import fastqc_report_tags


__author__ = 'med-pvo'


class FastqcReportFileManager(object):
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def file_path_for_tag(self, tag):
        tag = re.sub("img_tag$", "report", tag)
        file_path = os.path.join(self.output_dir, tag + ".html")
        return file_path


class FastqcReportWriter(object):
    def __init__(self, fastqc_summary, output_dir="./Fastqc_Writer_Report"):
        self.fastqc_summary = fastqc_summary
        self.file_manager = FastqcReportFileManager(output_dir)

    def write_report_for_tag(self, tag):
        file_path = self.file_manager.file_path_for_tag(tag)
        html_string = self.fastqc_summary.get_html_for_tag(tag)
        with open(file_path, "w") as html_file:
            print(html_string, file=html_file)
        print("Written: " + os.path.basename(file_path))

    def write(self):
        for tag in fastqc_report_tags():
            self.write_report_for_tag(tag)


if __name__ == "__main__":
    mateHandler = MateHandler()
    dirInfos = [MateDirInfo(mate) for mate in mateHandler.list_project_mates()]
    pairs = list(zip([dirInfo.first_fastqc_zip_path for dirInfo in dirInfos],
                     [dirInfo.second_fastqc_zip_path for dirInfo in dirInfos]))
    fastqcSummary = PairedFastqcSummary(pairs)
    writer = FastqcReportWriter(fastqcSummary, "TestData/FastqcSummary")
    writer.write()



