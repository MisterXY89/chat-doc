"""
Load and process ICD-11 data to generate a dataset for training and testing.
"""


import json
import os
import pickle
import random
import re

import numpy as np
import pandas as pd
from tqdm import tqdm

from chat_doc.config import DATA_DIR, logger
from chat_doc.dataset_generation.chat_dataset import ChatDataset


class ICD11Dataset(ChatDataset):
    def __init__(self, name="icd"):
        super().__init__(name)
        self.icd11_path = DATA_DIR + "/pinglab-ICD11-data.json"

    def load_data(self: str):
        """
        Load ICD-11 data from json file.

        Args:
            icd11_path (str): path to ICD-11 json file.
        """
        try:
            self.dataset = pd.read_json(self.icd11_path)
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise e

    def process_data(self):
        """
        Here we reproduce the data processing steps shown usefull from our exploration (data_exploration.ipynb)
        """
        if self._is_loaded():
            # copy data to avoid changing the original in case of errors
            icd11_data = self.dataset.copy()

        # we can only use a record if it has a definition, this also removes all nan values for sibls
        na_value = "Key Not found"
        icd11_data = icd11_data.query(f"definition != '{na_value}'")

        # remove unneded cols
        # we keep:  name, parents, sibls, definition, synonym
        icd11_data = icd11_data[["id", "tree", "root", "degree", "childs"]]

        self.processed = True
        self.dataset = icd11_data

    def build_prompts(self):
        if self._is_processed():
            icd11_data = self.dataset.copy()

        print(icd11_data.shape)
        return {"icd11": {"prompt": "ICD-11 code for", "answer": "definition"}}
