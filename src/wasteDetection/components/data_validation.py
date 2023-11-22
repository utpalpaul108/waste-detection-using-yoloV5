import os
from wasteDetection.entity import DataValidationConfig


# Data Validation Component
class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
        self.required_file_list = config.required_file_list

    def initiate_data_validation(self) -> bool:
        try:
            validation_status = True
            all_files_dir = os.listdir(self.config.dataset_dir)

            for required_file in self.required_file_list:
                if required_file not in all_files_dir:
                    validation_status = False
                    break
            
            with open(self.config.validation_status_file_path, 'w') as f:
                f.write(f'Validation status: {validation_status}')

            return validation_status
                

        except Exception as e:
            raise e