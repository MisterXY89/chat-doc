"""
Load and process PMC patients data to generate a dataset for training and testing.
"""

import re

import numpy as np
import pandas as pd
from datasets import load_dataset
from tqdm import tqdm

from chat_doc.config import logger
from chat_doc.dataset_generation.chat_dataset import ChatDataset


class PMCPatientsDataset(ChatDataset):
    def __init__(self, name="PMC"):
        super().__init__(name)
        self.hf_path = "zhengyun21/PMC-Patients"

    def load_data(self: str):
        """
        Loads data from HuggingFace Datasets library.
        See: https://github.com/zhao-zy15/PMC-Patients
        """
        raw_dataset = load_dataset(self.hf_path)
        raw_dataset = raw_dataset["train"]
        self.dataset = raw_dataset.to_pandas()

    def process_data(self):
        """
        Process data, following the steps identified in the exploration phase (see pmc_data_exploration.ipynb)
        """
        if self._is_loaded():
            pmc_data = self.dataset.copy()

        # age
        pmc_data.age = pmc_data.age.apply(lambda x: re.findall(r"\d+\.\d+", x)[0]).astype(float)

        # sex
        pmc_data.rename({"gender": "sex"}, inplace=True, axis=1)

        # sim patients
        pmc_data.similar_patients = pmc_data.similar_patients.apply(lambda x: len(x)).astype(int)

        # drop irrelevant columns
        pmc_data.drop(
            columns=["file_path", "patient_id", "patient_uid", "relevant_articles"], inplace=True
        )

        logger.info("PMC patients data processed.")
        self.processed = True
        self.dataset = pmc_data

    def build_prompts(self):
        if self._is_processed():
            pmc_data = self.dataset.copy()

        def _str_sex(sex_str: str) -> str:
            return "male" if sex_str == "M" else "female"

        prompts = []
        for _, row in tqdm(pmc_data.iterrows(), total=pmc_data.shape[0]):
            title = row["title"]
            patient = row["patient"]
            age = row["age"]
            sex = row["sex"]
            similar_patients = row["similar_patients"]

            prompt = f"Please describe a real-world patient case including symptoms about a {_str_sex(sex)} patient of {age} years old with the following title: {title}"
            response = f"{patient} The patient is similar to {similar_patients} other patients."

            prompts.append({"prompt": prompt, "response": response})

        logger.info("PMC patients prompts built.")
        self.prompts = prompts
