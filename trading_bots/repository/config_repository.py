import logging
import sys

import yaml


class ConfigRepository:

    def __init__(self, config_file_path: str):
        self.config_file_path = config_file_path

    def load_config(self) -> dict:
        try:
            logging.debug("Start loading config")
            with open(self.config_file_path, 'r') as stream:
                config = yaml.safe_load(stream)
                logging.debug(f"Loaded config: {config}")
                return config
        except Exception as e:
            logging.error(f"Failed to load config: {str(e)}")
            sys.exit(-1)
