import os
import pickle

import datasets
import pandas as pd

from chat_doc.config import DATA_DIR, ROOT_DIR, logger
from chat_doc.dataset_generation.icd11_dataset import ICD11Dataset
from chat_doc.dataset_generation.pmc_patients_dataset import PMCPatientsDataset


class DatasetFactory:
    def __init__(self):
        self.dataset = None
        self.path = ROOT_DIR + "/data/full_prompts.pkl"

    def build_full_dataset(self):
        # load both datasets
        icd_prompts = self.load_dataset("icd")
        pmc_prompts = self.load_dataset("pmc")
        print(len(icd_prompts))
        print(len(pmc_prompts))

        # combine them
        prompts = icd_prompts + pmc_prompts

        print(len(prompts))
        print(len(icd_prompts) + len(pmc_prompts))

        try:
            with open(self.path, "wb") as f:
                pickle.dump(prompts, f)
                logger.info(f"Full prompts saved to {self.path}")
        except Exception as e:
            logger.error(f"Could not save full prompts to {self.path}")
            logger.error(e)

        return prompts

    def load_full_dataset(self):
        try:
            with open(self.path, "rb") as f:
                prompts = pickle.load(f)
                logger.info(f"Full prompts loaded from {self.path}")
        except Exception as e:
            logger.error(f"Could not load full prompts from {self.path}")
            logger.error(e)
            prompts = None

        return prompts

    def build_dataset(self, name):
        if name == "icd":
            self.dataset = ICD11Dataset()
        elif name == "pmc":
            self.dataset = PMCPatientsDataset()
        elif name == "full":
            self.build_full_dataset()
        else:
            raise ValueError(
                f"Dataset {name} not supported. Please choose from: 'icd', 'pmc', 'full'"
            )

        self.dataset.load_data()
        self.dataset.process_data()
        self.dataset.build_prompts()

        # save both, preprocessed and prompts (ready to use)
        self.dataset.save(prompt=True)
        # self.dataset.save(output_path, prompt=True, fn_affix="v1")

        return self.dataset.prompts

    def convert_to_hf(self, dataset):
        logger.info("Converting to HuggingFace Dataset")
        print(type(dataset))
        print(len(dataset))
        hf_dataset = datasets.Dataset.from_pandas(pd.DataFrame(data=dataset))
        return hf_dataset

    def load_dataset(self, name, is_prompts=True):
        if name == "icd":
            self.dataset = ICD11Dataset()
        elif name == "pmc":
            self.dataset = PMCPatientsDataset()
        elif name == "full":
            return self.load_full_dataset()
        else:
            raise ValueError(f"Dataset {name} not supported.")

        self.dataset.load(is_prompts=is_prompts)

        return self.dataset.dataset
