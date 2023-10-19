"""
General config file: for all parts of the project
"""

import yaml
import logging
import logging.config
import pretty_errors

#--------- load config ---------#
# Change if you renamed your config filey
CONFIG_FILE_PATH = 'config.yml'

# Load and parse the YAML configuration file
def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config


config = load_config(CONFIG_FILE_PATH)

# saftey check
# --> ensure that the required keys exist in the configuration
required_keys = ['logging']
for key in required_keys:
    if key not in config:
        raise ValueError(f"Missing '{key}' in the configuration file.")

# Additional helper functions for specific configuration values, etc. can be defined here
# ...

#--------- set up logging ---------#
logging.config.dictConfig(config['logging'])
logger = logging.getLogger(__name__)
logger.info("logging setup complete")


logger.info("config loaded")