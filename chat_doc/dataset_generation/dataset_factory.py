import os
import pickle

from chat_doc.config import DATA_DIR, logger
from chat_doc.dataset_generation.icd11_dataset import ICD11Dataset
from chat_doc.dataset_generation.pmc_patients_dataset import PMCPatientsDataset


class DatasetFactory:
    def __init__(self):
        self.dataset = None

    def build_full_dataset(self, output_path):
        icd_prompts = self.build_dataset("icd", output_path)
        pmc_prompts = self.build_dataset("pmc", output_path)
        # prompts is list of dicts with keys: "prompt", "response"
        prompts = icd_prompts + pmc_prompts

        try:
            with open(os.path.join(output_path, "full_prompts.pkl"), "wb") as f:
                pickle.dump(prompts, f)
                logger.info(f"Full prompts saved to {output_path}/full_prompts.pkl")
        except Exception as e:
            logger.error(f"Could not save full prompts to {output_path}/full_prompts.pkl")
            logger.error(e)

        return prompts

    def load_full_dataset(self, output_path):
        try:
            with open(os.path.join(output_path, "full_prompts.pkl"), "rb") as f:
                prompts = pickle.load(f)
                logger.info(f"Full prompts loaded from {output_path}/full_prompts.pkl")
        except Exception as e:
            logger.error(f"Could not load full prompts from {output_path}/full_prompts.pkl")
            logger.error(e)
            prompts = None

        return prompts

    def build_dataset(self, name, output_path=DATA_DIR):
        if name == "icd":
            self.dataset = ICD11Dataset()
        elif name == "pmc":
            self.dataset = PMCPatientsDataset()
        elif name == "all":
            self.build_full_dataset(output_path)
        else:
            raise ValueError(
                f"Dataset {name} not supported. Please choose from: 'icd', 'pmc', 'all'"
            )

        self.dataset.load_data()
        self.dataset.process_data()
        self.dataset.build_prompts()

        # save both, preprocessed and prompts (ready to use)
        self.dataset.save(output_path)
        self.dataset.save(output_path, prompt=True, fn_affix="v1")

        return self.dataset.prompts

    def load_dataset(self, name, output_path="./"):
        if name == "icd":
            self.dataset = ICD11Dataset()
        elif name == "pmc":
            self.dataset = PMCPatientsDataset()
        elif name == "all":
            pass
        else:
            raise ValueError(f"Dataset {name} not supported.")

        self.dataset.load(output_path)
        return self.dataset.prompts
