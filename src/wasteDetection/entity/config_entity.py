from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    raw_dataset_dir: Path
    dataset_dir: Path


@dataclass(frozen=True)
class DataValidationConfig:
    dataset_dir: Path
    required_file_list: list
    root_dir: Path
    validation_status_file_path: Path


@dataclass(frozen=True)
class ModelTrainingConfig:
    root_dir: Path
    yolo_model_gitgub_url: str
    num_classes: int
    pretrained_model_name: str
    image_size: int
    batch_size: int
    epochs: int
    required_files: list
    dataset_dir: Path