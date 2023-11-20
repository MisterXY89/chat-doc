import pickle

import pandas as pd

from chat_doc.config import DATA_DIR, logger


class ChatDataset(object):
    def __init__(self, name, prompts=None) -> None:
        self.name = name
        self.dataset = None
        self.prompts = None
        self.processed = False

    def save(self, prompt=False, fn_affix=""):
        """
        self.dataset is a pandas DataFrame --> we use the pickle format to save it and keep the structure
        """
        path = DATA_DIR
        if prompt:
            try:
                with open(
                    f"{path}/{self._is_prompt_fn()}{self.name}{self._get_affix(fn_affix)}.pkl", "wb"
                ) as fi:
                    pickle.dump(self.prompts, fi)
                logger.info(f"Dataset {self.name} saved to file.")
            except Exception as e:
                logger.error(f"Error saving dataset: {e}")
        else:
            try:
                self.dataset.to_pickle(
                    f"{path}/{self._is_prompt_fn()}{self.name}{self._get_affix(fn_affix)}.pkl"
                )
                logger.info(f"Dataset {self.name} saved to file.")
            except Exception as e:
                logger.error(f"Error saving dataset: {e}")

    def load(self, fn_affix="", is_prompts=False):
        """
        self.dataset is a pandas DataFrame --> we use the pickle format to save it and keep the structure
        """
        path = DATA_DIR
        if is_prompts:
            self.prompts = True
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

    def unify_prompt(self, instruction, response, context=""):
        """
        Unify the prompt format for all datasets for instruct tuning.

        Args:
            instruction (str): instruction text
            response (str): response text
            context (str): context text (optional)

        Returns:
            str: multiline unified prompt string
        """
        instruction = f"### Instruction\n{instruction}"
        context = f"### Context\n{context}" if len(context) > 0 else None
        response = f"### Answer\n{response}"
        # join all the parts together
        prompt = "\n\n".join([i for i in [instruction, context, response] if i is not None])
        return prompt

    def get_dataset_name(self):
        return self.name

    def load_data(self):
        raise NotImplementedError

    def process_data(self):
        raise NotImplementedError

    def build_prompts(self):
        raise NotImplementedError
