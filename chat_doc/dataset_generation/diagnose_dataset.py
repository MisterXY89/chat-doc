"""
Load and process ICD-11 data to generate a dataset for training and testing.
"""

import numpy as np
import pandas as pd
from tqdm import tqdm

from chat_doc.config import BASE_DIR, logger, SEED
from chat_doc.dataset_generation.chat_dataset import ChatDataset

np.random.seed(SEED)


class DiagnoseDataset(ChatDataset):
    def __init__(self, name="diagnose"):
        super().__init__(name)
        self.diagnose_me_path = BASE_DIR + "/data/en_medical_dialog.json"

    def load_data(self: str):
        """
        Load Diagnose-Me data from json file.
        """
        try:
            self.dataset = pd.read_json(self.diagnose_me_path)
            logger.info("Diagnose-Me data loaded from json file.")
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise e

    def process_data(self):
        """
        Here we reproduce the data processing steps shown usefull from our exploration (data_exploration.ipynb)
        """
        if self._is_loaded():
            # copy data to avoid changing the original in case of errors
            diagnose_data = self.dataset.copy()

        # drop irrelevant columns (id) --> is the same as pd index
        diagnose_data.drop(columns=["id"], inplace=True)
        diagnose_data.columns = ["desc", "doctor", "patient"]

        for col in diagnose_data.columns:
            # remove all urls from text
            diagnose_data[col] = diagnose_data[col].str.replace(r'\s*https?://\S+(\s+|$)', ' ').str.strip()
            # remove all html tags from text
            diagnose_data[col] = diagnose_data[col].str.replace(r'<[^<]+?>', ' ').str.strip()


        logger.info("Diagnose-Me data processed.")
        self.processed = True
        self.dataset = diagnose_data

    def build_prompts(self):
        if self._is_processed():
            diagnose_data = self.dataset.copy()

        # sample 7% of the data --> approx. 15.000 prompts
        diagnose_data = diagnose_data.sample(frac=0.06).reset_index(drop=True)

        prompts = []
        for _, row in tqdm(diagnose_data.iterrows(), total=diagnose_data.shape[0]):                  

            prompts.append(
                # inherit from ChatDataset
                self.unify_prompt(
                    instruction=f"{row['desc']}",
                    context=f"Patient: {row['patient']}",
                    response=f"{row['doctor']}",
                )
            )

        logger.info("Diagnose-Me prompts built.")
        self.prompts = prompts
