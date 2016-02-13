import abc
import sys
import os
import bs4
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from tools.fastqc.fastqc_parser import FastQCReport

__author__ = 'med-pvo'

class FastqcSummary(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def combine(self, tag_name):
        """Method should combine zip files in the same report"""

    @abc.abstractmethod
    def get_html_for_tag(self, tag):
        """Method should return html tag from fastq report for a tag of interest"""


class PairedFastqcSummary(FastqcSummary):
    def __init__(self, file_pairs_list):
        self.file_pairs_list = file_pairs_list

    def report_pairs_list(self):
        return [(FastQCReport(file[0]), FastQCReport(file[1])) for file in self.file_pairs_list]

    def combine(self, tag):
        res = '<table style="width:100%">'
        for file_pair in self.file_pairs_list:
            first_report = FastQCReport(file_pair[0])
            second_report = FastQCReport(file_pair[1])
            res += '<tr><td>'
            res += os.path.basename(file_pair[0]) + '<br/>'
            res += str(getattr(first_report, tag)())
            res += '</td>'
            res += '<td>'
            res += os.path.basename(file_pair[1]) + '<br/>'
            res += str(getattr(second_report, tag)())
            res += '</td>'
        res += '</table>'
        return res

    def get_html_for_tag(self, tag):
        html_string = self.combine(tag)
        html_string = bs4.BeautifulSoup(html_string).prettify()
        return html_string
