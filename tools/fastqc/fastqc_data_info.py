__author__ = 'med-pvo'
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import re
from tools.fastqc.fastqc_zipfile import FastqcZipFile

class FastqcDataInfo():
    def __init__(self, text):
        text = str(text)
        self.__text = list(filter(None, text.split('\\n'))) ## text here comes as a list of lines

    @property
    def text(self):
        return self.__text

    def total_sequences(self):
        regex = re.compile("Total Sequences\D+(\d+)")
        res = list(filter(regex.search, self.text))[0]
        return int(str(regex.search(res).group(1)))
        #print(res)
        #print res
        #return str(filter(regex.search, self.text)[0])


if __name__ == "__main__":
    test_zip_file_path = "TestData/test_fastqc.zip"
    zf = FastqcZipFile(test_zip_file_path)
    txt = zf.data_txt
    info = FastqcDataInfo(txt)
    print(info.total_sequences())

