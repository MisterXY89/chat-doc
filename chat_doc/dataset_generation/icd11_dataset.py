"""
Load and process ICD-11 data to generate a dataset for training and testing.
"""

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
            logger.info("ICD-11 data loaded from json file.")
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
        icd11_data = icd11_data[["name", "parents", "sibls", "definition", "synonym"]]

        logger.info("ICD-11 data processed.")
        self.processed = True
        self.dataset = icd11_data

    def build_prompts(self):
        if self._is_processed():
            icd11_data = self.dataset.copy()

        prompts = []
        for _, row in tqdm(icd11_data.iterrows(), total=icd11_data.shape[0]):
            name = row["name"]
            definition = row["definition"]
            sibls = row["sibls"]
            synonym = row["synonym"]

            prompt = f"Describe {name} based on the international classification of deseases from the WHO in three sentences including the definition, siblings and the synonym."
            response = f"The definition for {name} is defined as: '{definition}'. The Sibling codes are {','.join(sibls)}. The Synonyms are {','.join(synonym)}."

            prompts.append({"prompt": prompt, "response": response})

        logger.info("ICD-11 prompts built.")
        self.prompts = prompts
