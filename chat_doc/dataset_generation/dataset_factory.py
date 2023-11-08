import os

from chat_doc.dataset_generation.icd11_dataset import ICD11Dataset
from chat_doc.dataset_generation.pmc_patients_dataset import PMCPatientsDataset


class DatasetFactory:
    def __init__(self):
        self.dataset = None

    def build_dataset(self, name, output_path="./"):
        if name == "icd":
            self.dataset = ICD11Dataset()
        elif name == "pmc":
            self.dataset = PMCPatientsDataset()
        else:
            raise ValueError(f"Dataset {name} not supported.")

        self.dataset.load_data()
        self.dataset.process_data()
        self.dataset.build_prompts()

        # save both, preprocessed and prompts (ready to use)
        self.dataset.save(output_path)
        self.dataset.save(output_path, prompt=True, fn_affix="v1")

        return self.dataset.prompts
