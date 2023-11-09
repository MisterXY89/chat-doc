import subprocess

import boto3
import sagemaker
from huggingface_hub import login


class TrainingsSetup:
    def __init__(self):
        pass

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

        print(f"sagemaker role arn: {self.role}")
        print(f"sagemaker bucket: {self.sess.default_bucket()}")
        print(f"sagemaker session region: {self.sess.boto_region_name}")

    def setup_hf(self):
        # login(token = access_token_read)
        output = subprocess.run(["huggingface-cli", "whoami"], check=True)
        if str(output) == "Not logged in":
            raise ValueError(
                "You are not logged in to the Hugging Face Hub. Please run `huggingface-cli login --token TOKEN` to login."
            )
        return True

    def setup(self):
        self.setup_hf()
        self.setup_aws()
