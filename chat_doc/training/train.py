from chat_doc.config import logger
from chat_doc.dataset_generation.dataset_factory import DatasetFactory
from chat_doc.training.setup_training import TrainingsSetup


class Trainer:
    def __init__(self, dataset, base_model, output_path):
        self.dataset = dataset
        self.base_model = base_model
        self.output_path = output_path
        self._is_initialized = False

    def _initialize(self):
        logger.info("Initializing trainer")
        self.trainings_config = TrainingsSetup()
        self.trainings_config.setup()
        self._is_initialized = True

    def train(self):
        if not self._is_initialized:
            self._initialize()
        logger.info(f"Training model on dataset: {self.dataset}")
        logger.info(f"Base model: {self.base_model}")
        logger.info(f"Output path: {self.output_path}")
