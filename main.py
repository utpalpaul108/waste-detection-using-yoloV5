from wasteDetection.pipeline.training_pipeline import TrainingPipeline


if __name__ == '__main__':
    # Training pipeline
    training_pipeline = TrainingPipeline()
    training_pipeline.train()