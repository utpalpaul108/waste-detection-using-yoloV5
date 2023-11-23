import os
import shutil
from pathlib import Path
from wasteDetection.constants import *
from wasteDetection.utils import read_yaml, encodeImageIntoBase64


class PredictionPipeline:

    def __init__(self):
        self.config = read_yaml(CONFIG_FILE_PATH)
        self.params = read_yaml(PARAMS_FILE_PATH)
        self.repo_name = self.config.model_training.yolo_model_gitgub_url.split('/')[-1].split('.')[0]


    def __get_required_files(self):
        self.best_weight_path = self.config.model_training.best_weight_file_path
        self.required_files = [self.best_weight_path, self.imgpath]

        for require_file_path in self.required_files:
            destination_file_path = os.path.join(self.repo_name, os.path.basename(require_file_path))
            shutil.copy2(require_file_path, destination_file_path)

    def __remove_required_files(self):
        os.system(f"rm -rf {self.repo_name}/runs")
        for require_file_path in self.required_files:
            file_path = os.path.join(self.repo_name, os.path.basename(require_file_path))
            if os.path.exists(file_path):
                os.remove(file_path)

    def predict(self, imgpath):
        
        self.imgpath = imgpath
        self.__get_required_files()
                    
        os.system(f"cd {self.repo_name}/ && python detect.py --weights {os.path.basename(self.best_weight_path)} --img {self.params.IMAGE_SIZE} --conf {self.params.MIN_CONFIDENCE_SCORE} --source {os.path.basename(self.imgpath)}")

        detected_image_path = Path(f"{self.repo_name}/runs/detect/exp/{os.path.basename(self.imgpath)}")
        opencodedbase64 = encodeImageIntoBase64(detected_image_path)
        result = {"image": opencodedbase64.decode('utf-8')}
        predicted_img_path = os.path.join(self.config.prediction.root_dir, 'predicted.jpg')
        shutil.copy2(detected_image_path, predicted_img_path)
        
        self.__remove_required_files()
        
        return result
    
    def livePredict(self):
        self.best_weight_path = self.config.model_training.best_weight_file_path
        destination_weight_path = os.path.join(self.repo_name, os.path.basename(self.best_weight_path))
        shutil.copy2(self.best_weight_path, destination_weight_path)

        os.system(f"cd {self.repo_name}/ && python detect.py --weights {os.path.basename(self.best_weight_path)} --img {self.params.IMAGE_SIZE} --conf {self.params.MIN_CONFIDENCE_SCORE} --source 0")

        os.system(f"rm -rf {self.repo_name}/runs")
        if os.path.exists(destination_weight_path):
            os.remove(destination_weight_path)

