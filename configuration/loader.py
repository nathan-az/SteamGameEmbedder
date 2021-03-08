import os
import pathlib
from dataclasses import dataclass
from typing import Optional

import dacite
import yaml


class ConfigurationLoader:
    @staticmethod
    def _get_config_dict(directory=None, filename=None):
        if directory is None:
            directory = pathlib.Path(__file__).parent
        if filename is None:
            filename = "config.yaml"
        path = os.path.join(directory, filename)
        with open(path) as stream:
            try:
                config = yaml.safe_load(stream)
                return config
            except yaml.YAMLError as e:
                print(e)

    def get_engine_configuration(self):
        config_dict = self._get_config_dict()
        config = dacite.from_dict(ConfigurationClass, config_dict)
        return config


@dataclass
class ConfigurationClass:
    API_KEY: str
    STARTING_ID: Optional[int]
    MAX_EMPTY_STREAK: int
    MAX_USERS_PER_SESSION: int


config = ConfigurationLoader().get_engine_configuration()
