import pickle

import pandas as pd

from chat_doc.config import DATA_DIR, logger


class ChatDataset(object):
    def __init__(self, name) -> None:
        self.name = name
        self.dataset = None
        self.processed = False

    def save(self, path=DATA_DIR):
        """
        self.dataset is a pandas DataFrame --> we use the pickle format to save it and keep the structure
        """
        try:
            self.dataset.to_pickle(f"{path}/{self.name}.pkl")
        except Exception as e:
            logger.error(f"Error saving dataset: {e}")

    def load(self, path=DATA_DIR):
        """
        self.dataset is a pandas DataFrame --> we use the pickle format to save it and keep the structure
        """
        try:
            self.dataset = pd.read_pickle(f"{path}/{self.name}.pkl")
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")

    def _is_processed(self):
        if not self.processed:
            raise AttributeError("Dataset not processed. Use process_data() method.")
        return True

    def _is_loaded(self):
        if self.dataset is None:
            raise AttributeError("Dataset not loaded. Use load() method.")
        return True

    def get_dataset_name(self):
        return self.name

    def load_data(self):
        raise NotImplementedError

    def process_data(self):
        raise NotImplementedError

    def build_prompts(self):
        raise NotImplementedError
