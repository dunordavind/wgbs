from pipeline.mate_dir_info import MateDirInfo
from structures.mate_handler import MateHandler
from tools.bismark.bismark_report import BismarkReport
from tools.bismark.deduplicate_report import DeduplicationReportParser
from tools.count_fastq_reads import count_fastq_reads


def print_sample_statistics(args):
    print("Counting statistics")
    sample_name = args.sampleName
    mate_handler = MateHandler()
    sample = mate_handler.get_sample_by_name(sample_name)

    total_first = 0
    total_second = 0
    total_aligned = 0
    total_deduplicated = 0

    for mate in sample.mates:
        di = MateDirInfo(mate)

        total_first += count_fastq_reads(di.first_fastqc_zip_path)
        total_second += count_fastq_reads(di.second_fastqc_zip_path)

        alignment_report = BismarkReport.fromfile(di.alignment_report_path)
        total_aligned += alignment_report.num_of_aligned

        drp = DeduplicationReportParser(di.deduplication_report_path)
        total_deduplicated += drp.sequences_left()

    print("Total first: ", total_first)
    print("Total second: ", total_second)
    print("Total algined: ", total_aligned)
    print("Total deduplicated: ", total_deduplicated)