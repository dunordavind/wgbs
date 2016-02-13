import bs4

__author__ = 'med-pvo'


class FastqcHTMLParser():
    def __init__(self, html_str):
        self.__html_parser = bs4.BeautifulSoup(html_str)

    @property
    def html_parser(self):
        return self.__html_parser

    @property
    def per_base_sequence_quality_img_tag(self):
        return self.get_image_tag_for_h2_with_id("M1").findNext('p')
        #return self.html_parser.find_all(id="M2")
            #self.get_image_tag_for_h2_with_id("M1")#.findNext('p')

    @property
    def per_tile_sequence_quality_img_tag(self):
        return self.get_image_tag_for_h2_with_id("M2").findNext('p')

    @property
    def per_sequence_quality_scores_img_tag(self):
        return self.get_image_tag_for_h2_with_id("M3").findNext('p')

    @property
    def per_sequence_quality_graph_img_tag(self):
        return self.get_image_tag_for_h2_with_id("M4").findNext('p')

    @property
    def per_sequence_gc_content_img_tag(self):
        return self.get_image_tag_for_h2_with_id("M5").findNext('p')

    @property
    def per_base_n_content_img_tag(self):
        return self.get_image_tag_for_h2_with_id("M6").findNext('p')

    @property
    def sequence_length_distribution_img_tag(self):
        return self.get_image_tag_for_h2_with_id("M7").findNext('p')

    @property
    def sequence_duplication_levels_img_tag(self):
        return self.get_image_tag_for_h2_with_id("M8").findNext('p')

    @property
    def overrepresented_sequences_img_tag(self):
        return self.get_image_tag_for_h2_with_id("M9").findNext('p')

    @property
    def adapter_graph_img_tag(self):
        return self.get_image_tag_for_h2_with_id("M10").findNext('p')

    @property
    def kmer_content_img_tag(self):
        return self.get_image_tag_for_h2_with_id("M11").findNext('p')

    def get_image_tag_for_h2_with_id(self, id_value):
        return self.html_parser.find(id=id_value).contents[0]