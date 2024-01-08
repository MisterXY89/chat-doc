import os
import pickle

import datasets
import pandas as pd

from chat_doc.config import DATA_DIR, ROOT_DIR, logger
from chat_doc.dataset_generation.baize_dataset import BaizeDataset
from chat_doc.dataset_generation.diagnose_dataset import DiagnoseDataset
from chat_doc.dataset_generation.icd11_dataset import ICD11Dataset
from chat_doc.dataset_generation.med_dialogue_dataset import MedDialogueDataset
from chat_doc.dataset_generation.pmc_patients_dataset import PMCPatientsDataset


class DatasetFactory:
    available_datasets = [
        "icd",
        "pmc",
        "diagnose",
        "med-dialogue",
        "baize",
        "dialogue-full",
        "full",
    ]

    def __init__(self):
        self.dataset = None
        self.full_path = ROOT_DIR + "/data/full_prompts.pkl"
        self.dialogue_path = ROOT_DIR + "/data/full_dialogue_prompts.pkl"

    def build_full_dialogue_dataset(self):
        dialogue_prompts = self.load_dataset("med-dialogue")
        diagnose_prompts = self.load_dataset("diagnose")

        if dialogue_prompts is None:
            dialogue_prompts = self.build_dataset("med-dialogue")
        if diagnose_prompts is None:
            diagnose_prompts = self.build_dataset("diagnose")

        # combine them
        prompts = dialogue_prompts + diagnose_prompts

        try:
            with open(self.dialogue_path, "wb") as f:
                pickle.dump(prompts, f)
                logger.info(f"Full prompts saved to {self.dialogue_path}")
        except Exception as e:
            logger.error(f"Could not save full prompts to {self.dialogue_path}")
            logger.error(e)

        return prompts

    def build_full_dataset(self):
        # load both datasets, if they don't exist, build them
        icd_prompts = self.load_dataset("icd")
        pmc_prompts = self.load_dataset("pmc")
        diagnose_prompts = self.load_dataset("diagnose")
        dialogue_prompts = self.load_dataset("med-dialogue")

        if icd_prompts is None:
            icd_prompts = self.build_dataset("icd")
        if pmc_prompts is None:
            pmc_prompts = self.build_dataset("pmc")
        if diagnose_prompts is None:
            diagnose_prompts = self.build_dataset("diagnose")
        if dialogue_prompts is None:
            dialogue_prompts = self.build_dataset("med-dialogue")

        print(len(icd_prompts))
        print(len(pmc_prompts))
        print(len(diagnose_prompts))
        print(len(dialogue_prompts))
        # combine them
        prompts = icd_prompts + pmc_prompts + diagnose_prompts + dialogue_prompts

        try:
            with open(self.full_path, "wb") as f:
                pickle.dump(prompts, f)
                logger.info(f"Full prompts saved to {self.full_path}")
        except Exception as e:
            logger.error(f"Could not save full prompts to {self.full_path}")
            logger.error(e)

        return prompts

    def load_full_dialogue_dataset(self):
        try:
            with open(self.dialogue_path, "rb") as f:
                prompts = pickle.load(f)
                logger.info(f"Full prompts loaded from {self.dialogue_path}")
        except Exception as e:
            logger.error(f"Could not load full dialogue prompts from {self.dialogue_path}")
            logger.error(e)
            prompts = None

        return prompts

    def load_full_dataset(self):
        try:
            with open(self.full_path, "rb") as f:
                prompts = pickle.load(f)
                logger.info(f"Full prompts loaded from {self.full_path}")
        except Exception as e:
            logger.error(f"Could not load full prompts from {self.full_path}")
            logger.error(e)
            prompts = None

        return prompts

    def _set_dataset(self, dataset_name):
        if dataset_name == "icd":
            return ICD11Dataset()
        elif dataset_name == "pmc":
            return PMCPatientsDataset()
        elif dataset_name == "diagnose":
            return DiagnoseDataset()
        elif dataset_name == "med-dialogue":
            return MedDialogueDataset()
        elif dataset_name == "baize":
            return BaizeDataset()

    def build_dataset(self, name):
        self.dataset = self._set_dataset(name)

        if self.dataset:
            self.dataset.load_data()
            self.dataset.process_data()
            self.dataset.build_prompts()

            # save both, preprocessed and prompts (ready to use)
            self.dataset.save(prompt=True)
            # self.dataset.save(output_path, prompt=True, fn_affix="v1")

            return self.dataset.prompts

        if name == "dialogue-full":
            return self.build_full_dialogue_dataset()
        elif name == "full":
            return self.build_full_dataset()
        else:
            raise ValueError(
                f"Dataset {name} not supported. Please choose from: {self.available_datasets}"
            )

    def convert_to_hf(self, dataset):
        logger.info("Converting to HuggingFace Dataset")
        hf_dataset = datasets.Dataset.from_pandas(pd.DataFrame(data=dataset))
        return hf_dataset

    def load_dataset(self, name, is_prompts=True):
        self.dataset = self._set_dataset(name)

        if self.dataset:
            self.dataset.load(is_prompts=is_prompts)
            return self.dataset.dataset

        if name == "dialogue-full":
            return self.load_full_dialogue_dataset()
        elif name == "full":
            return self.load_full_dataset()
        else:
            raise ValueError(
                f"Dataset {name} not supported. Please choose from: {self.available_datasets}"
            )
