import re
import zipfile

__author__ = 'med-pvo'


class FastqcZipFile():
    def __init__(self, zip_file_path):
        self.__zip_file_handler = zipfile.ZipFile(zip_file_path, 'r')

    @property
    def zip_file_handler(self):
        return self.__zip_file_handler

    @property
    def report_html(self):
        return self.extract_file_from_zip("fastqc_report.html")

    @property
    def data_txt(self):
        return self.extract_file_from_zip("fastqc_data.txt")

    def list_files(self):
        return [zipinfo.filename for zipinfo in self.zip_file_handler.filelist]

    def extract_file_from_zip(self, filename):
        found_paths = [file_path for file_path in self.list_files() if re.search(filename, file_path)]
        if len(found_paths) == 0:
            #possibly, instead of raising here, add checking for file name, if it is out of some list
            raise FileNotFoundError("There are no file with name " + filename + " in fastqc_archive")
        if len(found_paths) == 2:
            raise Exception("There are 2 files in fastq archive that have " + filename + "in it")
        file_path = found_paths[0]
        file_handler = self.zip_file_handler.open(file_path)
        file_data = file_handler.read()
        file_handler.close()
        return file_data

    def close(self):
        self.zip_file_handler.close()