"""
Load and process Baize medical chat data to generate a dataset for training and testing.
"""

import numpy as np
import pandas as pd
from tqdm import tqdm

from chat_doc.config import BASE_DIR, logger
from chat_doc.dataset_generation.chat_dataset import ChatDataset


class BaizeDataset(ChatDataset):
    def __init__(self, name="baize"):
        super().__init__(name)
        self.baize_path = BASE_DIR + "/data/baize_medical_chat_data.json"

    def load_data(self: str):
        """
        Load data from json file --> downloaded from here:
        https://github.com/project-baize/baize-chatbot/tree/main/data
        """
        try:
            self.dataset = pd.read_json(self.baize_path)
            # sample 10% of the data
            self.dataset = self.dataset.sample(frac=0.1, random_state=42)
            logger.info("Baize data loaded from json file.")
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise e

    def process_data(self):
        """
        Process data, mainly extract the chat "history"
        """
        if self._is_loaded():
            # copy data to avoid changing the original in case of errors
            baize_data = self.dataset.copy()

        baize_data = list(baize_data.input.values)

        conversation_list = []
        for data_record in tqdm(baize_data):
            msg_list = data_record.split("\n")[1:]
            tuple_list = []

            def clean_msg(msg):
                msg = msg.replace("[|Human|]", "").replace("[|AI|]", "").strip()
                return msg

            # remove empty messages + clean
            msg_list = [clean_msg(msg) for msg in msg_list if msg]

            for i, msg in enumerate(msg_list):
                if i % 2 != 0 and msg:
                    tuple_list.append((msg_list[i - 1], msg))

            conversation_list.append(tuple_list)

        logger.info("Baize data processed.")
        self.processed = True
        # self.dataset is a list of lists of tuples (instruction, response)
        self.dataset = conversation_list

    def build_prompts(self):
        if self._is_processed():
            # self.dataset is a list of lists of tuples (instruction, response)
            baize_data = self.dataset.copy()

        prompts = []
        for conversation in tqdm(baize_data):
            prompts.append(self.unify_prompt_v2(conversation))

        logger.info("Baize-medical prompts built.")
        self.prompts = prompts
