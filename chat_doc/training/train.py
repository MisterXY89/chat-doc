import time

from huggingface_hub import HfFolder
from sagemaker.huggingface import HuggingFace

from chat_doc.config import logger
from chat_doc.dataset_generation.dataset_factory import DatasetFactory
from chat_doc.training.pre_training import PreTrainingProcessor
from chat_doc.training.setup_training import TrainingsSetup


class Trainer:
    def __init__(self, dataset_name, base_model, hyperparams):
        # dataset is name (icd, pmc, full)
        self.dataset_name = dataset_name
        self.base_model = base_model
        self._is_initialized = False
        self._hyperparameters(**hyperparams)

    def _hyperparameters(self, epochs=3, per_device_train_batch_size=2, lr=2e-4):
        # hyperparameters, which are passed into the training job
        self.hyperparams = {
            "model_id": self.base_model,  # pre-trained model
            "dataset_path": "/opt/ml/input/data/training",  # path where sagemaker will save training dataset
            "epochs": epochs,  # number of training epochs
            "per_device_train_batch_size": per_device_train_batch_size,  # batch size for training
            "lr": lr,  # learning rate used during training
            "hf_token": HfFolder.get_token(),  # huggingface token to access llama 2
            "merge_weights": True,  # wether to merge LoRA into the model (needs more memory),
            "weight_decay": 0.01,  # weight decay used during training,
            "group_by_length": True,
        }

    def _hf_estimator(self, hyperparameters, job_name):
        # create the Estimator
        self.huggingface_estimator = HuggingFace(
            entry_point="run_clm.py",  # train script
            source_dir="chat_doc/training/",  # directory which includes all the files needed for training
            instance_type="ml.g5.4xlarge",  # instances type used for the training job
            # instance_type="ml.g4dn.xlarge",  # instances type used for the training job
            instance_count=1,  # the number of instances used for training
            base_job_name=job_name,  # the name of the training job
            role=self.trainings_config.role,  # Iam role used in training job to access AWS ressources, e.g. S3
            volume_size=300,  # the size of the EBS volume in GB
            transformers_version="4.28",  # the transformers version used in the training job
            pytorch_version="2.0",  # the pytorch_version version used in the training job
            py_version="py310",  # the python version used in the training job
            hyperparameters=hyperparameters,  # the hyperparameters passed to the training job
            environment={
                "HUGGINGFACE_HUB_CACHE": "/tmp/.cache",  # set env variable to cache models in /tmp
            },
        )

    def _build_training_job(self):
        # define Training Job Name
        job_name = f'huggingface-qlora-{time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())}'
        logger.info(f"Training Job Name: {job_name}")
        self._hf_estimator(self.hyperparams, job_name)

    def _initialize(self):
        logger.info("Loading dataset")
        self.dataset_factory = DatasetFactory()
        dataset_base = self.dataset_factory.load_dataset(self.dataset_name)
        # HF-Set
        self.dataset = self.dataset_factory.convert_to_hf(dataset_base)

        logger.info("Initializing trainer")
        self.trainings_config = TrainingsSetup(self.base_model, self.dataset_name)
        self.trainings_config.setup()
        self.training_input_path = self.trainings_config.training_input_path()

        logger.info("Initializing pre-training processor")
        self.pre_train_processor = PreTrainingProcessor(self.trainings_config.tokenizer)
        self.train_set = self.pre_train_processor.pre_train_dataset(self.dataset)

        self.trainings_config.upload_data(self.train_set)

        logger.info("Initializing complete.")
        self._is_initialized = True

    def train(self):
        if not self._is_initialized:
            self._initialize()

        logger.info(f"Training model on dataset: {self.dataset_name}")
        logger.info(f"Base model: {self.base_model}")

        self._build_training_job()
        data = {"training": self.training_input_path}
        # start training job
        self.huggingface_estimator.fit(data, wait=True)
