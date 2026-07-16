from textsummarizer.logging import logger
from textsummarizer.pipeline.prediction import PredictionPipeline

def main():
    logger.info("Welcome to AuraNews Intelligence Hub prediction pipeline")
    
    # Instantiate the PredictionPipeline
    try:
        pipeline = PredictionPipeline()
        
        # Test text processing
        test_text = "Welcome to AuraNews. This represents a modular pipeline test run for NLP preprocessing."
        stats = pipeline.run_preprocessing(test_text)
        
        logger.info("Modular pipeline initialized successfully!")
        logger.info(f"Preprocessing Test stats -> Words: {stats['word_count']}, Sentences: {stats['sentence_count']}")
    except Exception as e:
        logger.error(f"Failed to initialize modular pipeline: {e}")

if __name__ == "__main__":
    main()
