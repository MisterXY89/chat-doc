import pickle

import pandas as pd

from chat_doc.config import DATA_DIR, logger
from chat_doc.inference.prompt_template import PromptTemplate


class ChatDataset(object):
    def __init__(self, name, prompts=None) -> None:
        self.name = name
        self.dataset = None
        self.prompts = None
        self.processed = False
        self.training_system_prompt = "Below are a series of dialogues between various people and a medical AI doctor (Dr. Chad). The AI doctor (Dr. Chad) tries to be helpful, polite, honest, sophisticated, emotionally aware, and humble-but-knowledgeable. The AI doctor is happy to help with almost anything, and will do its best to understand exactly what is needed. It also tries to avoid giving false or misleading information, and it caveats when it isn't entirely sure about the right answer. That said, the assistant is practical and really does its best, and doesn't let caution get too much in the way of being useful."

    def save(self, prompt=False, fn_affix=""):
        """
        self.dataset is a pandas DataFrame --> we use the pickle format to save it and keep the structure
        """
        path = DATA_DIR
        if prompt:  # train ready prompts
            try:
                with open(
                    f"{path}/{self._is_prompt_fn()}{self.name}{self._get_affix(fn_affix)}.pkl", "wb"
                ) as fi:
                    pickle.dump(self.prompts, fi)
                logger.info(f"Dataset {self.name} saved to file.")
            except Exception as e:
                logger.error(f"Error saving dataset: {e}")
        else:  # save the processed dataset (-> as df)
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

        Returns:
            str: multiline unified prompt string
        """
        instruction = f"### Instruction\n{instruction}"
        context = f"### Context\n{context}" if len(context) > 0 else None
        response = f"### Answer\n{response}"
        # join all the parts together
        prompt = "\n\n".join([i for i in [instruction, context, response] if i is not None])
        return prompt

    def unify_prompt_v2(self, conversation):
        """
        conversation: list of tuples (instruction, response)
        """

        assert len(conversation) > 0, "Conversation must not be empty."

        # format conversation
        formatted_conversation = ""

        def formatted_conversation_template(instruction, response):
            return f"""<s>[INST] <<SYS>>
{self.training_system_prompt}
<</SYS>>

{instruction} [/INST] {response}) </s>"""

        for msg_tuple in conversation:
            formatted_conversation += formatted_conversation_template(msg_tuple[0], msg_tuple[1])

        return {
            "text": formatted_conversation,
        }

    def get_dataset_name(self):
        return self.name

    def load_data(self):
        raise NotImplementedError

    def process_data(self):
        raise NotImplementedError

    def build_prompts(self):
        raise NotImplementedError
