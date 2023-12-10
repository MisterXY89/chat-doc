"""
Load and process ICD-11 data to generate a dataset for training and testing.
"""

import numpy as np
import pandas as pd
from datasets import load_dataset
from tqdm import tqdm

from chat_doc.config import BASE_DIR, logger
from chat_doc.dataset_generation.chat_dataset import ChatDataset


class MedDialogueDataset(ChatDataset):
    def __init__(self, name="med-dialogue"):
        super().__init__(name)
        self.variant = "processed.en"
        self.med_dialogue_hf_id = "medical_dialog"

    def load_data(self: str):
        """
        Load Medical Dialogue data from HF dataset.
        """
        try:
            raw_dataset = load_dataset(self.med_dialogue_hf_id, self.variant)
            self.dataset = raw_dataset["train"]
            #  = raw_dataset.to_pandas()
            logger.info("Medical Dialogue data loaded from HF.")
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise e

    def process_data(self):
        """
        Here we reproduce the data processing steps shown usefull from our exploration (data_exploration.ipynb)
        """
        if self._is_loaded():
            med_dialogue = self.dataset

        diag_list = []
        for record in med_dialogue:
            utt = record["utterances"]
            diag_list.append(
                {
                    "patient": utt[0].replace("patient: ", ""),
                    "doctor": utt[1].replace("doctor: ", ""),
                }
            )

        med_dialogue = pd.DataFrame(diag_list)

        logger.info("Medical Dialogue data processed.")
        self.processed = True
        self.dataset = med_dialogue

    def build_prompts(self):
        if self._is_processed():
            med_dialogue = self.dataset.copy()

        prompts = []
        for _, row in tqdm(med_dialogue.iterrows(), total=med_dialogue.shape[0]):
            prompts.append(
                # inherit from ChatDataset
                self.unify_prompt(
                    instruction=f"{row['patient']}",
                    context="",
                    response=f"{row['doctor']}",
                )
            )

        logger.info("Medical Dialogue prompts built.")
        self.prompts = prompts
