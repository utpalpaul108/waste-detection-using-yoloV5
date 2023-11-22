import subprocess
import shutil
import yaml
import os
from pathlib import Path
from wasteDetection.entity import ModelTrainingConfig


# Model Training Component
class ModelTraining:
    def __init__(self, config: ModelTrainingConfig):
        self.config = config

    def _get_yolo_model_from_gitgub(self):
        self.repo_name = self.config.yolo_model_gitgub_url.split('/')[-1].split('.')[0]
        if (not os.path.exists(self.repo_name)):
            subprocess.call(["git", "clone", self.config.yolo_model_gitgub_url])
            shutil.rmtree(os.path.join(self.repo_name,'.git'))

    def _make_custom_model_config(self):
        pretrained_model_path = Path(f'yolov5/models/{self.config.pretrained_model_name}.yaml')
        
        with open(pretrained_model_path) as f:
            pretrained_model_config = yaml.safe_load(f)
        
        pretrained_model_config['nc'] = self.config.num_classes
        custom_model_config_path = Path(f'yolov5/models/custom_{self.config.pretrained_model_name}.yaml')
        
        with open(custom_model_config_path, 'w') as f:
                yaml.dump(pretrained_model_config, f)

    def _train_model(self):
        for require_file in self.config.required_files:
            require_file_path = os.path.join(self.config.dataset_dir, require_file)
            destination_file_path = os.path.join(self.repo_name, require_file)
            if not os.path.exists(destination_file_path):
                if os.path.isdir(require_file_path):
                    shutil.copytree(require_file_path, destination_file_path)
                else:
                    shutil.copy(require_file_path, destination_file_path)
                
        os.system(f"cd {self.repo_name}/ && python train.py --img {self.config.image_size} --batch {self.config.batch_size} --epochs {self.config.epochs} --data data.yaml --cfg models/custom_{self.config.pretrained_model_name}.yaml --weights '{self.config.pretrained_model_name}.pt' --name {self.config.pretrained_model_name}_results --cache")
        
    def _model_training_post_processing(self):
        os.system(f"cp {self.repo_name}/runs/train/{self.config.pretrained_model_name}_results/weights/best.pt {self.config.root_dir}/")
        required_files = self.config.required_files
        required_files.append('runs')

        for require_file in required_files:
            require_file_path = os.path.join(self.repo_name,require_file)
            if os.path.exists(require_file_path):
                if os.path.isdir(require_file_path):
                    shutil.rmtree(require_file_path)
                else:
                    os.remove(require_file_path)
        

    def initiate_model_training(self):
        try:
            self._get_yolo_model_from_gitgub()
            self._make_custom_model_config()
            self._train_model()
            self._model_training_post_processing()
        except Exception as e:
            raise e
