import gdown
from wasteDetection.logger import logger
import zipfile
import shutil
import os
from wasteDetection.entity import DataIngestionConfig
from wasteDetection.utils import create_directories, read_yaml


# Data Ingestion Component
class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def _download_dataset(self) -> None:
        '''
        Fetch the dataset from the URL
        '''

        try:
            if (not os.path.exists(self.config.dataset_dir)) or (not os.listdir(self.config.dataset_dir)):
                create_directories([self.config.raw_dataset_dir])
                
                dataset_url = self.config.source_url
                output_path = os.path.join(self.config.raw_dataset_dir, 'data.zip')
                file_id = dataset_url.split('/')[-2]
                prefix = 'https://drive.google.com/uc?/export=download&id='
                gdown.download(prefix+file_id, output_path, quiet=False)

                logger.info("Dataset downloaded successful")


        except Exception as e:
            raise e
        

    def _preprocess_dataset(self):
        '''
        Preprocess the raw dataset
        '''
        if os.path.exists(self.config.raw_dataset_dir):
            try:
                create_directories([self.config.dataset_dir])
                for root, dirs, files in os.walk(self.config.raw_dataset_dir):
                    for file in files:
                        
                        # Check if the file is an zip file
                        if file.lower().endswith(('.zip')):
                            file_path = os.path.join(root, file)
                            with zipfile.ZipFile(file_path) as zip_ref:
                                zip_ref.extractall(self.config.dataset_dir)

                shutil.rmtree(self.config.raw_dataset_dir)
            
            except Exception as e:
                raise e
            
    
    def initiate_data_ingestion(self) -> None:
        self._download_dataset()
        self._preprocess_dataset()
    