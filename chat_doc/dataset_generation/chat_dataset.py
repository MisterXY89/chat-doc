import pickle

import pandas as pd

from chat_doc.config import logger


class ChatDataset(object):
    def __init__(self, name) -> None:
        self.name = name
        self.dataset = None

    def get_dataset_name(self):
        return self.name

    def load_data(self):
        raise NotImplementedError

    def process_data(self):
        raise NotImplementedError

    def build_prompts(self):
        raise NotImplementedError

    def save(self, path="./"):
        """
        self.dataset is a pandas DataFrame --> we use the pickle format to save it and keep the structure
        """
        try:
            self.dataset.to_pickle(path + self.name + ".pkl")
        except Exception as e:
            logger.error(f"Error saving dataset: {e}")
