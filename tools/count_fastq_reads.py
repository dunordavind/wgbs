__author__ = 'med-pvo'

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tools.run_shell_command import run_shell_command
from tools.fastqc.fastqc_zipfile import FastqcZipFile
from tools.fastqc.fastqc_data_info import FastqcDataInfo

def count_fastq_reads(file_path):
    zf = FastqcZipFile(file_path)
    txt = zf.data_txt
    info = FastqcDataInfo(txt)
    return info.total_sequences()

