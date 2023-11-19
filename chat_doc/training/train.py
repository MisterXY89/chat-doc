from chat_doc.config import logger
from chat_doc.dataset_generation.dataset_factory import DatasetFactory
from chat_doc.training.pre_training import PreTrainingProcessor
from chat_doc.training.setup_training import TrainingsSetup


class Trainer:
    def __init__(self, dataset_name, base_model, output_path):
        # dataset is name (icd, pmc, full)
        self.dataset_name = dataset_name
        self.base_model = base_model
        self.output_path = output_path
        self._is_initialized = False

    def _initialize(self):
        logger.info("Loading dataset")
        self.dataset_factory = DatasetFactory()
        self.dataset = self.dataset_factory.load_full_dataset(self.dataset_name)

        logger.info("Initializing pre-training processor")
        self.pre_train_processor = PreTrainingProcessor(self.trainings_config.tokenizer)
        self.train_set = self.pre_train_processor.pre_train_dataset(self.dataset)

        logger.info("Initializing trainer")
        self.trainings_config = TrainingsSetup()
        self.trainings_config.setup()

        self.trainings_config.upload_data(self.train_set)

        logger.info("Initializing complete.")
        self._is_initialized = True

    def train(self):
        if not self._is_initialized:
            self._initialize()
        logger.info(f"Training model on dataset: {self.dataset}")
        logger.info(f"Base model: {self.base_model}")
        logger.info(f"Output path: {self.output_path}")
