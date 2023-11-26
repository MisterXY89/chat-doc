import os
import sys
import unittest

# append to path to import from chat_doc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_doc.config import logger
from chat_doc.dataset_generation.dataset_factory import DatasetFactory
from chat_doc.training.train import Trainer


def _delete_existing_data():
    # delete everything in DATA_DIR
    for file in os.listdir(os.path.join(os.getcwd(), "data")):
        print(file)
        # os.remove(os.path.join(os.getcwd(), "data", file))


# class DataGeneration(unittest.TestCase):
class DataGeneration:
    def build_icd(self):
        dataset_factory = DatasetFactory()
        dataset_factory.build_dataset(name="icd")
        logger.info("icd data generated.")

    def build_pmc(self):
        dataset_factory = DatasetFactory()
        dataset_factory.build_dataset(name="pmc")
        logger.info("pmc data generated.")

    def build_full(self):
        dataset_factory = DatasetFactory()
        dataset_factory.build_dataset(name="full")
        logger.info("full data generated.")

    logger.log("Data generation complete.")

    # train model
    trainer = Trainer(dataset_name="full")
    trainer.train()
    logger.log("Training complete.")

    # evaluate model
    logger.log("Evaluation ...")


if __name__ == "__main__":
    # unittest.main()
    _delete_existing_data()
