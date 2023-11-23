import os
import yaml
import json
import joblib
import base64
from pathlib import Path
from typing import Any
from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError
from wasteDetection.logger import logger


@ensure_annotations
def read_yaml(yaml_file_path: Path)->ConfigBox:
    """reads yaml file and return as ConfigBox instance
    
    Args:
        yaml_file_path (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: invalid file type
    
    Returns:
        ConfigBox: ConfigBox instance
    
    """
    try:
        with open(yaml_file_path, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f'YAML file: {yaml_file_path} loaded successfully')
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError('YAML file is empty')
    except Exception as e:
        raise e
    

@ensure_annotations
def save_yaml(yaml_file_path: Path, content: object, replace: bool = False) -> None:
    """save data to yaml file
        
    Args:
        yaml_file_path (str): path like input
        content (object): contents of the file
        replace (bool): replace the content or not
        
    """
    try:
        if replace:
            if os.path.exists(yaml_file_path):
                os.remove(yaml_file_path)

        os.makedirs(os.path.dirname(yaml_file_path), exist_ok=True)

        with open(yaml_file_path, 'w') as f:
            yaml.dump(content, f)
            logger.info(f'{yaml_file_path} file saved successfully')
            
    except Exception as e:
        raise e



@ensure_annotations
def create_directories(directories_path: list, verbose=True):
    """creates list of directories
       
       Args:
            directories_path (list): list of directories path
            verbose (bool): status to show the directory creation log
    
    """
    for directory_path in directories_path:
        os.makedirs(directory_path, exist_ok=True)
        if verbose:
            logger.info(f'created directory at: {directory_path}')



@ensure_annotations
def save_json(path: Path, data: dict):
    """save data to json format
    
       Args:
            path (Path): path to save
            data (dict): data to be saved in json file
    
    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
        logger.info(f'json file saved at: {path}')


@ensure_annotations
def load_json(path: Path)->ConfigBox:
    """load json file data
    
       Args:
            path (Path): json file path

       Returns:
            ConfigBox: ConfigBox instance
    
    """
    with open(path, 'r') as f:
        content = json.load(path)
        logger.info(f'json file loaded successfully from: {path}')
        return ConfigBox(content)


@ensure_annotations
def save_binary(path: Path, data: Any):
    """save binary data
    
       Args:
            path (Path): path to save binary data
            data (Any): data to be saved as binary
    """
    joblib.dump(value=data, filename=path)
    logger.info(f'binary file saved at: {path}')


@ensure_annotations
def load_bin(path: Path)->Any:
    """load binary data

       Args:
            path (Path): path to load binary data
        
       Returns:
            Any: object stored in the file
    """
    content = joblib.load(path)
    logger.info(f'binary file loaded from: {path}')
    return content


@ensure_annotations
def get_size(path: Path)->str:
    """get size in KB

    Args:
        path (Path): path of the file
    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f'~ {size_in_kb} KB'


@ensure_annotations
def decodeImage(img_str: str, file_name: str):
    """save as image file from image string data
    
       Args:
            img_str (str): image data in string format
            file_name (str): path to save the image

    """
    img_data = base64.b64decode(img_str)
    with open(file_name, 'wb') as f:
        f.write(img_data)


@ensure_annotations
def encodeImageIntoBase64(img_path: Path):

    """return image as base64 encoded string

       Args:
            img_path (Path): path of the image
    
       Returns:
            str: base64 encoded string
    """
    with open(img_path, 'rb') as f:
        img_content = f.read()
        return base64.b64encode(img_content)