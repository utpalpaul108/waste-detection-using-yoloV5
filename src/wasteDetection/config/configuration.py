from wasteDetection.constants import *
from wasteDetection.utils import create_directories, read_yaml
from wasteDetection.entity import DataIngestionConfig, DataValidationConfig, ModelTrainingConfig


# Configuration Manager
class ConfigurationManager:
    def __init__(self, config_filepath = CONFIG_FILE_PATH, params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir = Path(config.root_dir),
            source_url = config.source_URL,
            raw_dataset_dir = Path(config.raw_dataset_dir),
            dataset_dir = Path(config.dataset_dir)
        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        
        create_directories([self.config.data_validation.root_dir])

        data_validation_config = DataValidationConfig(
            dataset_dir = Path(self.config.data_ingestion.dataset_dir),
            required_file_list = self.params.REQUIRED_FILES,
            root_dir = Path(self.config.data_validation.root_dir),
            validation_status_file_path = Path(self.config.data_validation.validation_status_file_path)

        )

        return data_validation_config
    
    def get_model_training_config(self) -> ModelTrainingConfig:
        create_directories([self.config.model_training.root_dir])
        data_file_path = Path(self.config.data_ingestion.dataset_dir, 'data.yaml')
        data_config = read_yaml(data_file_path)

        model_training_config = ModelTrainingConfig(
            root_dir = Path(self.config.model_training.root_dir),
            yolo_model_gitgub_url = self.config.model_training.yolo_model_gitgub_url,
            num_classes =  int(data_config.nc),
            pretrained_model_name = self.params.PRETRAINED_MODEL_NAME,
            image_size = self.params.IMAGE_SIZE,
            batch_size = self.params.BATCH_SIZE,
            epochs = self.params.EPOCHS,
            required_files = self.params.REQUIRED_FILES,
            dataset_dir = self.config.data_ingestion.dataset_dir
        )

        return  model_training_config