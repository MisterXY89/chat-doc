"""
Load and process PMC patients data to generate a dataset for training and testing.
"""


import json
import os
import pickle
import random
import re

import numpy as np
import pandas as pd
from datasets import load_dataset
from tqdm import tqdm

from chat_doc.dataset_generation.chat_dataset import ChatDataset


class PMCPatientsDataset(ChatDataset):
    def __init__(self, name="icd"):
        super().__init__(name)
        self.hf_path = "zhengyun21/PMC-Patients"

    def load_data(self: str):
        """
        Loads data from HuggingFace Datasets library.
        See: https://github.com/zhao-zy15/PMC-Patients
        """
        self.dataset = load_dataset(self.hf_path)

    def process_data(self):
        if self._is_loaded():
            pmc_data = self.dataset.copy()

        self.dataset = pmc_data

    def build_prompts(self):
        if self._is_processed():
            pmc_data = self.dataset.copy()

        print(pmc_data.shape)

        return {"pmc": {"prompt": "PMC code for", "answer": "definition"}}
