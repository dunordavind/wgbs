__author__ = 'med-pvo'

import re
import unittest
import glob

class TrimGaloreReportParser:
    def __init__(self, file_path):
        self.__file_path = file_path
        with open (self.file_path, "r") as input_file:
            self.__report = input_file.read() #.replace('\n', '')

    @property
    def file_path(self):
        return self.__file_path

    @property
    def report(self):
        return self.__report

    def adapter_trimmed(self):
        adapter_counts = {}
        for search in re.finditer("Adapter \'(\w+)\',.*was trimmed (\d+) times\.", self.report):
            adapter_counts[search.group(1)] = int(search.group(2))
        return adapter_counts


class TrimGaloreReport:
    def __init__(self):
        self.adapter_trimmed = None

    @classmethod
    def fromparser(cls, parser):
        report = TrimGaloreReport()
        report.adapter_trimmed = parser.adapter_trimmed()
        return report

    @classmethod
    def fromfile(cls, file_path):
        parser = TrimGaloreReportParser(file_path)
        return cls.fromparser(parser)

    def __add__(self, other):
        res = TrimGaloreReport()
        res.adapter_trimmed = dict([(key, value + other.adapter_trimmed[key])
                                    for (key, value) in self.adapter_trimmed.items()])
        return res

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            raise ValueError('Cannot Radd ' + str(other) + ' to object of class TrimGaloreReport')


class TrimGaloreReportMerger:
    def __init__(self, directory):
        self.__directory = directory if directory.endswith('/') else directory

    @property
    def directory(self):
        return self.__directory

    def list_reports(self):
        report_files = glob.glob(self.directory + "*trimming_report.txt")
        return [TrimGaloreReport.fromfile(report_file) for report_file in report_files]

    def merge_reports(self):
        reports = self.list_reports()
        return sum(reports)


class TestTrimGaloreReportMerger(unittest.TestCase):
    def setUp(self):
        self.final_report_parser = TrimGaloreReportParser("TestData/valid_trim_galore_report.txt")
        self.report_merger = TrimGaloreReportMerger("TestData/TrimGaloreReports/")
        self.merged_report = self.report_merger.merge_reports()

    def test_that_adds_adapter_counts(self):
        self.assertEqual(self.final_report_parser.adapter_trimmed()["AGATCGGAAGAGC"],
                         self.merged_report.adapter_trimmed["AGATCGGAAGAGC"])


class TestTrimGaloreReportParser(unittest.TestCase):
    def setUp(self):
        self.good_parser = TrimGaloreReportParser("TestData/valid_trim_galore_report.txt")
        self.good_parser_two_adapters = TrimGaloreReportParser("TestData/valid_trim_galore_duplicated_adapter_line.txt")

    def test_that_returns_correct_adapter_results(self):
        self.assertEqual(self.good_parser.adapter_trimmed()["AGATCGGAAGAGC"], 25976841)
        self.assertEqual(self.good_parser_two_adapters.adapter_trimmed()["AGATCGGAAGAGC"], 25976841)
        self.assertEqual(self.good_parser_two_adapters.adapter_trimmed()["SOMEOTHERADAPTER"], 666)


if __name__ == "__main__":
    unittest.main()

