import glob

import unittest
import re


class BismarkReport:
    def __init__(self):
        self.met_unmet_cs_ratio_chh_context = None
        self.met_unmet_cs_ratio_chg_context = None
        self.met_unmet_cs_ratio_cpg_context = None
        self.total_unmet_cs_unknown_context = None
        self.total_unmet_cs_chh_context = None
        self.total_unmet_cs_chg_context = None
        self.total_unmet_cs_cpg_context = None
        self.total_met_cs_unknown_context = None
        self.total_met_cs_chh_context = None
        self.total_met_cs_chg_context = None
        self.total_met_cs_cpg_context = None
        self.total_cs_analysed = None
        self.num_of_bottom_strand = None
        self.num_of_compl_to_bottom_strand = None
        self.num_of_compl_to_top_strand = None
        self.num_of_top_strand = None
        self.num_of_crossmapped = None
        self.number_unique_matches = None
        self.num_of_unaligned = None
        self.total_pairs_analyzed = None
        self.num_of_nonextractable = None
        self.num_of_aligned = None

    @classmethod
    def fromfile(cls, file_path):
        """
        :type cls: BismarkReport
        :param file_path:
        :return: BismarkReport object
        :raise ValueError:
        """
        parser = BismarkReportParser(file_path)
        if not parser.is_valid():
            raise ValueError("Wrong file format")
        br = cls.fromparser(parser)
        return br

    @classmethod
    def fromparser(cls, parser):
        """

        :rtype : BismarkReport
        """
        if not parser.is_valid():
            raise ValueError("Wrong file format")
        br = BismarkReport()

        br.total_pairs_analyzed = parser.total_pairs_analyzed()
        br.number_unique_matches = parser.number_unique_matches()
        br.num_of_unaligned = parser.num_of_unaligned()
        br.num_of_crossmapped = parser.num_of_crossmapped()
        br.num_of_nonextractable = parser.num_of_nonextractable()
        br.num_of_top_strand = parser.num_of_top_strand()
        br.num_of_compl_to_top_strand = parser.num_of_compl_to_top_strand()
        br.num_of_compl_to_bottom_strand = parser.num_of_compl_to_bottom_strand()
        br.num_of_bottom_strand = parser.num_of_bottom_strand()
        br.total_cs_analysed = parser.total_cs_analysed()
        br.total_met_cs_cpg_context = parser.total_met_cs_cpg_context()
        br.total_met_cs_chg_context = parser.total_met_cs_chg_context()
        br.total_met_cs_chh_context = parser.total_met_cs_chh_context()
        br.total_met_cs_unknown_context = parser.total_met_cs_unknown_context()
        br.total_unmet_cs_cpg_context = parser.total_unmet_cs_cpg_context()
        br.total_unmet_cs_chg_context = parser.total_unmet_cs_chg_context()
        br.total_unmet_cs_chh_context = parser.total_unmet_cs_chh_context()
        br.total_unmet_cs_unknown_context = parser.total_unmet_cs_unknown_context()
        br.met_unmet_cs_ratio_cpg_context = parser.met_unmet_cs_ratio_cpg_context()
        br.met_unmet_cs_ratio_chg_context = parser.met_unmet_cs_ratio_chg_context()
        br.met_unmet_cs_ratio_chh_context = parser.met_unmet_cs_ratio_chh_context()
        br.num_of_aligned = parser.number_unique_matches() - parser.num_of_nonextractable()
        return br

    def __add__(self, other):
        res = BismarkReport()
        res.total_pairs_analyzed = self.total_pairs_analyzed + other.total_pairs_analyzed
        res.number_unique_matches = self.number_unique_matches + other.number_unique_matches
        res.num_of_unaligned = self.num_of_unaligned + other.num_of_unaligned
        res.num_of_crossmapped = self.num_of_crossmapped + other.num_of_crossmapped
        res.num_of_nonextractable = self.num_of_nonextractable + other.num_of_nonextractable
        res.num_of_top_strand = self.num_of_top_strand + other.num_of_top_strand
        res.num_of_compl_to_top_strand = self.num_of_compl_to_top_strand + other.num_of_compl_to_top_strand
        res.num_of_compl_to_bottom_strand = self.num_of_compl_to_bottom_strand + other.num_of_compl_to_bottom_strand
        res.num_of_bottom_strand = self.num_of_bottom_strand + other.num_of_bottom_strand
        res.total_cs_analysed = self.total_cs_analysed + other.total_cs_analysed
        res.total_met_cs_cpg_context = self.total_met_cs_cpg_context + other.total_met_cs_cpg_context
        res.total_met_cs_chg_context = self.total_met_cs_chg_context + other.total_met_cs_chg_context
        res.total_met_cs_chh_context = self.total_met_cs_chh_context + other.total_met_cs_chh_context
        res.total_met_cs_unknown_context = self.total_met_cs_unknown_context + other.total_met_cs_unknown_context
        res.total_unmet_cs_cpg_context = self.total_unmet_cs_cpg_context + other.total_unmet_cs_cpg_context
        res.total_unmet_cs_chg_context = self.total_unmet_cs_chg_context + other.total_unmet_cs_chg_context
        res.total_unmet_cs_chh_context = self.total_unmet_cs_chh_context + other.total_unmet_cs_chh_context
        res.total_unmet_cs_unknown_context = self.total_unmet_cs_unknown_context + other.total_unmet_cs_unknown_context
        res.met_unmet_cs_ratio_cpg_context = round(self.total_met_cs_cpg_context * 100.0 /
                                                   (self.total_met_cs_cpg_context + self.total_unmet_cs_cpg_context), 1)
        res.met_unmet_cs_ratio_chg_context = round(self.total_met_cs_chg_context * 100.0 /
                                                   (self.total_met_cs_chg_context + self.total_unmet_cs_chg_context), 1)
        res.met_unmet_cs_ratio_chh_context = round(self.total_met_cs_chh_context * 100.0 /
                                                   (self.total_met_cs_chh_context + self.total_unmet_cs_chh_context), 1)
        res.num_of_aligned = self.num_of_aligned + other.num_of_aligned
        return res

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            raise ValueError("Cannot add " + str(other) + " to object of class BismarkReport()")


class BismarkReportParser:
    def __init__(self, file_path):
        self.__file_path = file_path
        with open(self.file_path, "r") as input_file:
            self.__report = input_file.read().replace('\n', '')

    def is_valid(self):
        return True if re.match("Bismark report for:", self.report) else False

    @property
    def file_path(self):
        return self.__file_path

    @property
    def report(self):
        return self.__report

    def total_pairs_analyzed(self):
        res = re.search("Sequence pairs analysed in total:\s+(\d+)", self.report)
        return int(res.group(1))

    def number_unique_matches(self):
        res = re.search("Number of paired-end alignments with a unique best hit:\s+(\d+)", self.report)
        return int(res.group(1))

    def num_of_unaligned(self):
        res = re.search("Sequence pairs with no alignments under any condition:\s+(\d+)", self.report)
        return int(res.group(1))

    def num_of_crossmapped(self):
        res = re.search("Sequence pairs did not map uniquely:\s+(\d+)", self.report)
        return int(res.group(1))

    def num_of_nonextractable(self):
        res = re.search("Sequence pairs which were discarded because genomic sequence could not be extracted:\s+(\d+)",
                        self.report)
        return int(res.group(1))

    def num_of_top_strand(self):
        res = re.search("CT/GA/CT:\s+(\d+)", self.report)
        return int(res.group(1))

    def num_of_compl_to_top_strand(self):
        res = re.search("GA/CT/CT:\s+(\d+)", self.report)
        return int(res.group(1))

    def num_of_compl_to_bottom_strand(self):
        res = re.search("GA/CT/GA:\s+(\d+)", self.report)
        return int(res.group(1))

    def num_of_bottom_strand(self):
        res = re.search("CT/GA/GA:\s+(\d+)", self.report)
        return int(res.group(1))

    def total_cs_analysed(self):
        res = re.search("Total number of C's analysed:\s+(\d+)", self.report)
        return int(res.group(1))

    def total_met_cs_cpg_context(self):
        res = re.search("Total methylated C's in CpG context:\s+(\d+)", self.report)
        return int(res.group(1))

    def total_met_cs_chg_context(self):
        res = re.search("Total methylated C's in CHG context:\s+(\d+)", self.report)
        return int(res.group(1))

    def total_met_cs_chh_context(self):
        res = re.search("Total methylated C's in CHH context:\s+(\d+)", self.report)
        return int(res.group(1))

    def total_met_cs_unknown_context(self):
        res = re.search("Total methylated C's in Unknown context:\s+(\d+)", self.report)
        return int(res.group(1))

    def total_unmet_cs_cpg_context(self):
        res = re.search("Total unmethylated C's in CpG context:\s+(\d+)", self.report)
        return int(res.group(1))

    def total_unmet_cs_chg_context(self):
        res = re.search("Total unmethylated C's in CHG context:\s+(\d+)", self.report)
        return int(res.group(1))

    def total_unmet_cs_chh_context(self):
        res = re.search("Total unmethylated C's in CHH context:\s+(\d+)", self.report)
        return int(res.group(1))

    def total_unmet_cs_unknown_context(self):
        res = re.search("Total unmethylated C's in Unknown context:\s+(\d+)", self.report)
        return int(res.group(1))

    def met_unmet_cs_ratio_cpg_context(self):
        unmet = self.total_unmet_cs_cpg_context()
        met = self.total_met_cs_cpg_context()
        res = met * 100.0 / (met + unmet)
        return round(res, 1)

    def met_unmet_cs_ratio_chg_context(self):
        unmet = self.total_unmet_cs_chg_context()
        met = self.total_met_cs_chg_context()
        res = met * 100.0 / (met + unmet)
        return round(res, 1)

    def met_unmet_cs_ratio_chh_context(self):
        unmet = self.total_unmet_cs_chh_context()
        met = self.total_met_cs_chh_context()
        res = met * 100.0 / (met + unmet)
        return round(res, 1)


class BismarkParserTest(unittest.TestCase):
    def setUp(self):
        self.good_file_path = "TestData/valid_report.txt"
        self.file_without_header = "TestData/report_without_header_line.txt"
        self.brp = BismarkReportParser(self.good_file_path)
        self.brp_no_header = BismarkReportParser(self.file_without_header)

    def test_if_correct_file_is_valid(self):
        self.assertTrue(self.brp.is_valid())

    def test_if_file_without_header_is_invalid(self):
        self.assertFalse(self.brp_no_header.is_valid())

    def test_file_path(self):
        self.assertEqual( self.brp.file_path, self.good_file_path)

    def test_total_pairs_analyzed(self):
        self.assertEqual( self.brp.total_pairs_analyzed(), 12749)

    def test_number_unique_matches(self):
        self.assertEqual( self.brp.number_unique_matches(), 9524)

    def test_num_of_unaligned(self):
        self.assertEqual( self.brp.num_of_unaligned(), 2277)

    def test_num_of_crossmapped(self):
        self.assertEqual( self.brp.num_of_crossmapped(), 948)

    def test_num_of_nonextractable(self):
        self.assertEqual( self.brp.num_of_nonextractable(), 0)

    def test_num_of_top_strand(self):
        self.assertEqual( self.brp.num_of_top_strand(), 4728)

    def test_num_of_compl_to_top_strand(self):
        self.assertEqual( self.brp.num_of_compl_to_top_strand(), 0)

    def test_num_of_compl_to_bottom_strand(self):
        self.assertEqual( self.brp.num_of_compl_to_bottom_strand(), 0)

    def test_num_of_bottom_strand(self):
        self.assertEqual( self.brp.num_of_bottom_strand(), 4796)

    def test_total_cs_analysed(self):
        self.assertEqual( self.brp.total_cs_analysed(), 362916)

    def test_total_met_cs_cpg_context(self):
        self.assertEqual( self.brp.total_met_cs_cpg_context(), 16197)

    def test_total_met_cs_chg_context(self):
        self.assertEqual( self.brp.total_met_cs_chg_context(), 1732)

    def test_total_met_cs_chh_context(self):
        self.assertEqual( self.brp.total_met_cs_chh_context(), 3131)

    def test_total_met_cs_unknown_context(self):
        self.assertEqual( self.brp.total_met_cs_unknown_context(), 0)

    def test_total_unmet_cs_cpg_context(self):
        self.assertEqual( self.brp.total_unmet_cs_cpg_context(), 5653)

    def test_total_unmet_cs_chg_context(self):
        self.assertEqual( self.brp.total_unmet_cs_chg_context(), 87502)

    def test_total_unmet_cs_chh_context(self):
        self.assertEqual( self.brp.total_unmet_cs_chh_context(), 248701)

    def test_total_unmet_cs_unknown_context(self):
        self.assertEqual( self.brp.total_unmet_cs_unknown_context(), 0)

    def test_met_unmet_cs_ratio_cpg_context(self):
        self.assertEqual( self.brp.met_unmet_cs_ratio_cpg_context(), 74.1)

    def test_met_unmet_cs_ratio_chg_context(self):
        self.assertEqual( self.brp.met_unmet_cs_ratio_chg_context(), 1.9)

    def test_met_unmet_cs_ratio_chh_context(self):
        self.assertEqual( self.brp.met_unmet_cs_ratio_chh_context(), 1.2)

if __name__ == "__main__":
    #file_path = "TestData/valid_report.txt"
    #brp = BismarkReportParser(file_path)
    #br = BismarkReport.fromparser(brp)
    #br.list_report_files()
    #print br.number_unique_matches
    #br.test_me()
    #bra = BismarkReportMerger("TestData/BismarkReports/")
    #res = bra.merge_reports("asdf")
    #print(res.total_pairs_analyzed)
    unittest.main()