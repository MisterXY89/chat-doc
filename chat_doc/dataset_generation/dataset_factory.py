import os
import pickle

import pandas as pd

from chat_doc.config import DATA_DIR, ROOT_DIR, logger
from chat_doc.dataset_generation.icd11_dataset import ICD11Dataset
from chat_doc.dataset_generation.pmc_patients_dataset import PMCPatientsDataset


class DatasetFactory:
    def __init__(self):
        self.dataset = None

    def build_full_dataset(self, output_path):
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
            with open(os.path.join(output_path, "full_prompts.pkl"), "wb") as f:
                pickle.dump(prompts, f)
                logger.info(f"Full prompts saved to {output_path}/full_prompts.pkl")
        except Exception as e:
            logger.error(f"Could not save full prompts to {output_path}/full_prompts.pkl")
            logger.error(e)

        return prompts

    def load_full_dataset(self):
        try:
            with open(os.path.join(ROOT_DIR, "/data/full_prompts.pkl"), "rb") as f:
                prompts = pickle.load(f)
                logger.info(f"Full prompts loaded from {ROOT_DIR}/data/full_prompts.pkl")
        except Exception as e:
            logger.error(f"Could not load full prompts from {ROOT_DIR}/data/full_prompts.pkl")
            logger.error(e)
            prompts = None

        return prompts

    def build_dataset(self, name, output_path=DATA_DIR):
        if name == "icd":
            self.dataset = ICD11Dataset()
        elif name == "pmc":
            self.dataset = PMCPatientsDataset()
        elif name == "full":
            self.build_full_dataset(output_path)
        else:
            raise ValueError(
                f"Dataset {name} not supported. Please choose from: 'icd', 'pmc', 'full'"
            )

        self.dataset.load_data()
        self.dataset.process_data()
        self.dataset.build_prompts()

        # save both, preprocessed and prompts (ready to use)
        self.dataset.save(output_path, prompt=True)
        # self.dataset.save(output_path, prompt=True, fn_affix="v1")

        return self.dataset.prompts

    def load_dataset(self, name, output_path="./", is_prompts=True):
        if name == "icd":
            self.dataset = ICD11Dataset()
        elif name == "pmc":
            self.dataset = PMCPatientsDataset()
        elif name == "all":
            return self.load_full_dataset(output_path)
        else:
            raise ValueError(f"Dataset {name} not supported.")

        self.dataset.load(is_prompts=is_prompts)

        return self.dataset.dataset
