from collections import namedtuple
from unicodedata import name


# Training Pipeline Config
TrainingPipelineConfig= namedtuple('TrainingPipelineConfig',
['training_artifact_dir'])


# Data Ingestion Config
DataIngestionConfig= namedtuple('DataIngestionConfig',
['download_data_url', 'raw_data_dir', 'ingested_train_dir', 'ingested_test_dir'])


# Data Validation Config
DataValidationConfig= namedtuple('DataValidationConfig',
['schema_file_path', 'report_file_path', 'report_page_file_path'])

