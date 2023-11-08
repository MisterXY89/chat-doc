"""
MAIN FILE: --> ACEESIBLE & CALLED BY END USER

also testing during dev
"""

import os
import sys

from config import config, logger
from data_collection.docx_reader import DocXReader
from data_collection.url_collect import UrlCollect

if __name__ == "__main__":
    logger.info("loaded")

    reader = DocXReader(config, logger)
    data = reader.read(
        "/Users/tilmankerl/Documents/UNI/03_WS23/Applied Deep Learning/project/data/print_ICD11_Primary_Care_Low_RS-en.docx"
    )
    print(data)
