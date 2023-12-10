import json

import boto3
import sagemaker
from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri


class SageMakerDeployment:
    def __init__(self, s3_model_uri, instance_type="ml.g5.4xlarge"):
        self.s3_model_uri = s3_model_uri
        self.instance_type = instance_type
        self.sess = sagemaker.Session()
        self.sagemaker_session_bucket = self._get_sagemaker_session_bucket()
        self.role = self._get_sagemaker_role()
        self.llm_image = self._get_llm_image_uri()
        self.config = self._get_model_config()

    def _get_sagemaker_session_bucket(self):
        # Return the default SageMaker session bucket
        return self.sess.default_bucket()

    def _get_sagemaker_role(self):
        # Retrieve the SageMaker execution role
        try:
            return sagemaker.get_execution_role()
        except ValueError:
            iam = boto3.client("iam")
            return iam.get_role(RoleName="sagemaker_execution_role")["Role"]["Arn"]

    def _get_llm_image_uri(self):
        # Retrieve the LLM image URI
        return get_huggingface_llm_image_uri("huggingface", version="1.0.3")

    def _get_model_config(self):
        # Define model and endpoint configuration parameters
        return {
            "HF_MODEL_ID": "/opt/ml/model",
            "MAX_INPUT_LENGTH": json.dumps(1024),
            "MAX_TOTAL_TOKENS": json.dumps(2048),
            "HF_MODEL_QUANTIZE": "bitsandbytes",
        }

    def deploy_model(self, health_check_timeout=300):
        # Deploy the HuggingFace model
        llm_model = HuggingFaceModel(
            role=self.role, image_uri=self.llm_image, model_data=self.s3_model_uri, env=self.config
        )
        return llm_model.deploy(
            initial_instance_count=1,
            instance_type=self.instance_type,
            container_startup_health_check_timeout=health_check_timeout,
        )


# Usage
s3_model_uri = "s3://sagemaker-eu-central-1-228610994900/huggingface-qlora-2023-12-08-15-01-13-2023-12-08-15-01-14-300/output/model.tar.gz"
deployment = SageMakerDeployment(s3_model_uri)
llm_endpoint = deployment.deploy_model()
