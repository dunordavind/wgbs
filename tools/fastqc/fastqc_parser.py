from tools.fastqc.fastqc_html_parser import FastqcHTMLParser
from tools.fastqc.fastqc_zipfile import FastqcZipFile

__author__ = 'med-pvo'

def callmethod(o, name):
    getattr(o, name)()


class FastQCReport:
    def __init__(self, zip_file_path):
        fastqc_zip_file = FastqcZipFile(zip_file_path)
        html = fastqc_zip_file.report_html
        html_parser = FastqcHTMLParser(html)
        fastqc_zip_file.close()

        ##setup image tags
        self.__per_base_sequence_quality_img_tag = html_parser.per_base_sequence_quality_img_tag
        self.__per_tile_sequence_quality_img_tag = html_parser.per_tile_sequence_quality_img_tag
        self.__per_sequence_quality_scores_img_tag = html_parser.per_sequence_quality_scores_img_tag
        self.__per_sequence_quality_graph_img_tag = html_parser.per_sequence_quality_graph_img_tag
        self.__per_sequence_gc_content_img_tag = html_parser.per_sequence_gc_content_img_tag
        self.__per_base_n_content_img_tag = html_parser.per_base_n_content_img_tag
        self.__sequence_duplication_levels_img_tag = html_parser.sequence_duplication_levels_img_tag
        self.__sequence_length_distribution_img_tag = html_parser.sequence_length_distribution_img_tag
        self.__overrepresented_sequences_img_tag = html_parser.overrepresented_sequences_img_tag
        self.__adapter_graph_img_tag = html_parser.adapter_graph_img_tag
        self.__kmer_content_img_tag = html_parser.kmer_content_img_tag

    def per_base_sequence_quality_img_tag(self):
        return self.__per_base_sequence_quality_img_tag

    def per_tile_sequence_quality_img_tag(self):
        return self.__per_tile_sequence_quality_img_tag

    def per_sequence_quality_scores_img_tag(self):
        return self.__per_sequence_quality_scores_img_tag

    def per_sequence_quality_graph_img_tag(self):
        return self.__per_sequence_quality_graph_img_tag

    def per_sequence_gc_content_img_tag(self):
        return self.__per_sequence_gc_content_img_tag

    def per_base_n_content_img_tag(self):
        return self.__per_base_n_content_img_tag

    def sequence_duplication_levels_img_tag(self):
        return self.__sequence_duplication_levels_img_tag

    def sequence_length_distribution_img_tag(self):
        return self.__sequence_length_distribution_img_tag

    def overrepresented_sequences_img_tag(self):
        return self.__overrepresented_sequences_img_tag

    def adapter_graph_img_tag(self):
        return self.__adapter_graph_img_tag

    def kmer_content_img_tag(self):
        return self.__kmer_content_img_tag