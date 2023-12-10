"""
Load and process PMC patients data to generate a dataset for training and testing.
"""

import re

import numpy as np
import pandas as pd
from datasets import load_dataset
from tqdm import tqdm
from transformers import AutoTokenizer, BigBirdPegasusForConditionalGeneration

from chat_doc.config import logger
from chat_doc.dataset_generation.chat_dataset import ChatDataset


class PMCPatientsDataset(ChatDataset):
    def __init__(self, name="pmc"):
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

        # num of sim patients
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

            prompts.append(
                # inherit from ChatDataset
                self.unify_prompt(
                    instruction=f"Please describe a real-world patient case including symptoms about a {_str_sex(sex)} patient of {age} years old with the following title: {title}",
                    context="",
                    response=f"{patient} The patient is similar to {similar_patients} other patients.",
                )
            )

        logger.info("PMC patients prompts built.")
        self.prompts = prompts

    def __next_build_prompts(self):
        if self._is_processed():
            pmc_data = self.dataset.copy()

        def _str_sex(sex_str: str) -> str:
            return "male" if sex_str == "M" else "female"

        # Sample prompt templates
        # templates = [
        #     "Summarize the medical history for a {age}-year-old {gender} patient based on the following summary: {patient_summary}",
        #     "Explain the treatment options for a patient with this profile: {patient_summary}",
        # ]

        prompts = []
        for _, row in pmc_data.iterrows():
            # template = np.random.choice(templates)
            age = row.age
            sex = _str_sex(row["sex"])
            patient_summary = row["patient"]
            instruction_template = f"Identify potential diagnoses for a {age}-year-old {sex} patient presenting these symptoms: {patient_summary}"

            prompts.append(
                # inherit from ChatDataset
                self.unify_prompt(
                    instruction=instruction_template,
                    context="",
                    response=f"{patient_summary}",
                )
            )

        return prompts
