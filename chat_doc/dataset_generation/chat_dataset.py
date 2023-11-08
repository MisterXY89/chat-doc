import pickle

import pandas as pd

from chat_doc.config import DATA_DIR, logger


class ChatDataset(object):
    def __init__(self, name) -> None:
        self.name = name
        self.dataset = None
        self.prompts = None
        self.processed = False

    def save(self, path=DATA_DIR, prompt=False, fn_affix=""):
        """
        self.dataset is a pandas DataFrame --> we use the pickle format to save it and keep the structure
        """

        try:
            self.dataset.to_pickle(
                f"{path}/{self._is_prompt_fn()}{self.name}{self._get_affix(fn_affix)}.pkl"
            )
            logger.info(f"Dataset {self.name} saved to file.")
        except Exception as e:
            logger.error(f"Error saving dataset: {e}")

    def load(self, path=DATA_DIR, fn_affix=""):
        """
        self.dataset is a pandas DataFrame --> we use the pickle format to save it and keep the structure
        """
        try:
            self.dataset = pd.read_pickle(
                f"{path}/{self._is_prompt_fn()}{self.name}{self._get_affix(fn_affix)}.pkl"
            )
            logger.info(f"Dataset {self.name} loaded from file.")
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")

    def _get_affix(self, affix):
        return f"_{affix}" if affix else ""

    def _is_processed(self):
        if not self.processed:
            raise AttributeError("Dataset not processed. Use process_data() method.")
        return True

    def _is_loaded(self):
        if self.dataset is None:
            raise AttributeError("Dataset not loaded. Use load() method.")
        return True

    def _is_prompt_fn(self):
        return "prompt_" if self.prompts else ""

    def get_dataset_name(self):
        return self.name

    def load_data(self):
        raise NotImplementedError

    def process_data(self):
        raise NotImplementedError

    def build_prompts(self):
        raise NotImplementedError
