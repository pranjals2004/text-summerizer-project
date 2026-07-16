from textsummarizer.config.configuration import ConfigurationManager
from textsummarizer.components.nlp_preprocessing import NLPPreprocessing

class PredictionPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.preprocessing_config = self.config_manager.get_nlp_preprocessing_config()
        self.preprocessing = NLPPreprocessing(config=self.preprocessing_config)

    def run_preprocessing(self, text: str):
        """Runs the complete NLP preprocessing pipeline on the input text."""
        return self.preprocessing.preprocess_text(text)

    def run_extractive_summary(self, text: str, num_sentences: int = 3):
        """Generates a quick local extractive summary."""
        return self.preprocessing.get_local_extractive_summary(text, num_sentences)
