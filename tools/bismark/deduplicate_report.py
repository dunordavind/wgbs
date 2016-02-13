__author__ = 'petr_v'
import os
import sys
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class DeduplicationReportParser:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(self.file_path, "r") as input_file:
            self.__report = input_file.read() #.replace('\n', '')

    @property
    def report(self):
        return self.__report

    def total_alignments_analyzed(self):
        res = re.search("Total number of alignments analysed in.+:\s+(\d+)", self.report)
        return int(res.group(1))

    def total_duplicates_removed(self):
        res = re.search("Total number duplicated alignments removed:\s+(\d+)", self.report)
        return int(res.group(1))

    def sequences_left(self):
        res = re.search("Total count of deduplicated leftover sequences:\s+(\d+)", self.report)
        return int(res.group(1))