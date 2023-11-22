from wasteDetection.config import ConfigurationManager
from wasteDetection.components.data_ingestion import DataIngestion
from wasteDetection.components.data_validation import DataValidation
from wasteDetection.components.model_training import ModelTraining


class TrainingPipeline:
    def train(self):
        try:
            config = ConfigurationManager()

            # Data Ingestion
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.initiate_data_ingestion()


            # Data Validation
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValidation(config=data_validation_config)
            status = data_validation.initiate_data_validation()


            # Model Training
            if status == True:
                model_training_config = config.get_model_training_config()
                model_training = ModelTraining(config=model_training_config)
                model_training.initiate_model_training()

        except Exception as e:
            raise e