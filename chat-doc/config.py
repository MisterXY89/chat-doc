"""
General config file: for all parts of the project
"""


import yaml

# Change if you renamed your config file
CONFIG_FILE_PATH = 'config.yml'

# Load and parse the YAML configuration file
def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config


config = load_config(CONFIG_FILE_PATH)


# SAFTY CHECKS
# Ensure that the required keys exist in the configuration
required_keys = ['database_url', 'api_key', 'other_config_key']
for key in required_keys:
    if key not in config:
        raise ValueError(f"Missing '{key}' in the configuration file.")

# Additional helper functions for specific configuration values, etc. can be defined here
# ...
