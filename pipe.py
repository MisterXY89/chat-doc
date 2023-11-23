from chat_doc.config import logger
from chat_doc.dataset_generation.dataset_factory import DatasetFactory
from chat_doc.training.train import Trainer


def end_to_end_pipe():
    # generate data
    dataset_factory = DatasetFactory()
    for dataset in dataset_factory.available_datasets:
        dataset_factory.build_dataset(name=dataset)
        logger.info(f"{dataset} data generated.")

    logger.log("Data generation complete.")

    # train model
    trainer = Trainer(dataset_name="full")
    trainer.train()
    logger.log("Training complete.")

    # evaluate model
    logger.log("Evaluation ...")


if __name__ == "__main__":
    end_to_end_pipe()
