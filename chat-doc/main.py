"""
MAIN FILE: --> ACEESIBLE & CALLED BY END USER

also testing during dev
"""

import os
import sys

from config import config, logger
from data_collection.url_collect import UrlCollect

if __name__ == "__main__":
    logger.info("loaded")

    url_collect = UrlCollect(
        url = 'https://icd.who.int/browse11/l-m/en',
        output_file = "urls.txt",
    )

    url_collect.collect()

