from textsummarizer.constants import *
from textsummarizer.utils.common import read_yaml, create_directories
from textsummarizer.entity import NLPPreprocessingConfig
from pathlib import Path

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_nlp_preprocessing_config(self) -> NLPPreprocessingConfig:
        config = self.config.nlp_preprocessing

        create_directories([config.root_dir])

        nlp_preprocessing_config = NLPPreprocessingConfig(
            root_dir=Path(config.root_dir),
            status_file=Path(config.status_file)
        )

        return nlp_preprocessing_config
