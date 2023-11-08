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

from chat_doc.dataset_generation.chat_dataset import ChatDataset


class ICD11Dataset(ChatDataset):
    def __init__(self, path, name="icd"):
        super().__init__(path, name)

    def load_data(self, icd11_path: str):
        """
        Load ICD-11 data from json file.

        Args:
            icd11_path (str): path to ICD-11 json file.
        """
        return pd.read_json(icd11_path)

    def process_data(self, icd11_data: pd.DataFrame):
        """
        Here we reproduce the data processing steps shown usefull from our exploration (data_exploration.ipynb)

        Args:
            icd11_data (pd.DataFrame): ICD-11 data.
        """
        # we can only use a record if it has a definition, this also removes all nan values for sibls
        na_value = "Key Not found"
        icd11_data = icd11_data.query(f"definition != '{na_value}'")

        # remove unneded cols
        # we keep:  name, parents, sibls, definition, synonym
        icd11_data = icd11_data[["id", "tree", "root", "degree", "childs"]]

        return icd11_data

    def build_prompts(self):
        return {"icd11": {"prompt": "ICD-11 code for", "answer": "definition"}}
