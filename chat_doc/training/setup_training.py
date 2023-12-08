import subprocess

import boto3
import sagemaker
from datasets import load_from_disk
from huggingface_hub import login as hf_login
from transformers import AutoTokenizer

from chat_doc.config import config, logger


class TrainingsSetup:
    def __init__(self, model_id, dataset_name):  # sharded weights
        self.model_id = model_id
        self.dataset_name = dataset_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=True)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        logger.info(f"Loaded tokenizer: {self.tokenizer}")

    def setup_aws(self):
        self.sess = sagemaker.Session()

        # sagemaker session bucket -> used for uploading data, models and logs
        # sagemaker will automatically create this bucket if it not exists
        sagemaker_session_bucket = None
        if sagemaker_session_bucket is None and self.sess is not None:
            # set to default bucket if a bucket name is not given
            sagemaker_session_bucket = self.sess.default_bucket()

        try:
            self.role = sagemaker.get_execution_role()
        except ValueError:
            self.iam = boto3.client("iam")
            self.role = self.iam.get_role(RoleName="sagemaker_execution_role")["Role"]["Arn"]

        self.sess = sagemaker.Session(default_bucket=sagemaker_session_bucket)

        logger.info(f"sagemaker role arn: {self.role}")
        logger.info(f"sagemaker bucket: {self.sess.default_bucket()}")
        logger.info(f"sagemaker session region: {self.sess.boto_region_name}")

    def setup_hf(self):
        hf_login(token=config["credentials"]["hf_token"])
        output = subprocess.run(["huggingface-cli", "whoami"], check=True)
        if str(output) == "Not logged in":
            raise ValueError(
                "You are not logged in to the Hugging Face Hub. Please run `huggingface-cli login --token TOKEN` to login."
            )
        logger.info("Logged in to Hugging Face Hub.")
        return True

    def training_input_path(self, dataset_name=None):
        if dataset_name is None:
            dataset_name = self.dataset_name
        return f"s3://{self.sess.default_bucket()}/processed/llama/{dataset_name}/train"

    def upload_data(self, train_set, dataset_name=None):
        if dataset_name is None:
            dataset_name = self.dataset_name
        # save train_dataset to s3
        train_set.save_to_disk(self.training_input_path(dataset_name))

        print("uploaded data to:")
        print(f"training dataset to: {self.training_input_path(dataset_name)}")

    def load_data(self, dataset_name=None):
        if dataset_name is None:
            dataset_name = self.dataset_name
        # load train_dataset from s3
        s3_path = self.training_input_path(dataset_name)
        train_set = load_from_disk(s3_path)
        logger.info(f"Loaded train_set from {s3_path}")
        return train_set

    def setup(self):
        self.setup_hf()
        self.setup_aws()
