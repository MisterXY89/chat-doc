"""
Pre-training utilities.
"""

from functools import partial
from itertools import chain
from random import randint

import datasets

from chat_doc.config import config, logger


class PreTrainingProcessor:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.remainder = {"input_ids": [], "attention_mask": [], "token_type_ids": []}

    def chunk(self, sample, chunk_length=2048):
        # Concatenate all texts and add remainder from previous batch
        concatenated_examples = {k: list(chain(*sample[k])) for k in sample.keys()}
        concatenated_examples = {
            k: self.remainder[k] + concatenated_examples[k] for k in concatenated_examples.keys()
        }

        logger.info(f"Concatenated examples: {len(concatenated_examples['input_ids'])}")

        # get total number of tokens for batch
        batch_total_length = len(concatenated_examples[list(sample.keys())[0]])

        # get max number of chunks for batch
        if batch_total_length >= chunk_length:
            batch_chunk_length = (batch_total_length // chunk_length) * chunk_length

        # Split by chunks of max_len.
        result = {
            k: [t[i : i + chunk_length] for i in range(0, batch_chunk_length, chunk_length)]
            for k, t in concatenated_examples.items()
        }
        logger.info(f"Chunked examples: {len(result['input_ids'])}")

        # add remainder to global variable for next batch
        self.remainder = {
            k: concatenated_examples[k][batch_chunk_length:] for k in concatenated_examples.keys()
        }
        # prepare labels
        result["labels"] = result["input_ids"].copy()
        return result

    def pre_train_dataset(self, dataset):
        logger.info(f"Dataset loaded: {len(dataset)}")
        # print random sample
        print(dataset[randint(0, len(dataset))]["text"])

        # tokenize and chunk dataset
        lm_dataset = dataset.map(
            lambda sample: self.tokenizer(sample["text"]),
            batched=True,
            remove_columns=list(dataset.features),
        ).map(
            partial(self.chunk, chunk_length=2048),
            batched=True,
        )

        # Print total number of samples
        logger.info(f"Total number of samples: {len(lm_dataset)}")

        return lm_dataset
