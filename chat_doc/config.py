"""
General config file: for all parts of the project
"""
import logging
import logging.config
import os

import pretty_errors
import yaml
from decouple import (
    config as decouple_config,  # Import the config function from decouple
)

# --------- load config ---------#
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# parent dir of chat_doc (BASE_DIR)
DATA_DIR = ROOT_DIR + "/data"

SEED = 1160

# Change if you renamed your config filey
CONFIG_FILE_PATH = f"{BASE_DIR}/config.yml"
CREDENTIAL_FILE_PATH = f"{BASE_DIR}/.env"
print(CREDENTIAL_FILE_PATH)


# parse the YAML configuration file
def parse_yaml_config(config_file_path):
    with open(config_file_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


def load_config():
    yaml_config = parse_yaml_config(CONFIG_FILE_PATH)

    # Combine data from .env and YAML into a single config object
    config = {
        "credentials": {
            "hf_token": decouple_config("HF_TOKEN"),
            # ...
        },
        "flask_app": {
            "flask_secret": decouple_config("SECRET_KEY"),
            "csfr_secret": decouple_config("WTF_CSRF_SECRET_KEY"),
            "app_name": decouple_config("FLASK_APP_NAME"),
            "db_name": decouple_config("FLASK_APP_DB_NAME"),
        },
        **yaml_config,
    }

    return config


config = load_config()

# Additional helper functions for specific configuration values, etc. can be defined here
# ...

# --------- set up logging ---------#
logging.config.dictConfig(config["logging"])
logger = logging.getLogger(__name__)
logger.info("logging setup complete")


logger.info("config loaded")
