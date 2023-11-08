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
from tqdm import tqdm

from chat_doc.dataset_generation.chat_dataset import ChatDataset


class PMCPatientsDataset(ChatDataset):
    def __init__(self, path, name="icd"):
        super().__init__(path, name)

    def load_data(self, icd11_path: str):
        pass

    def process_data(self, icd11_data: pd.DataFrame):
        pass

    def build_prompts(self):
        pass
