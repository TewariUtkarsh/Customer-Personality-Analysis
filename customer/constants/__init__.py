import os
from datetime import datetime


def get_current_timestamp() -> str:
    curr_time= datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    return curr_time


# General Constants
ROOT_DIR= os.getcwd()
CURRENT_TIMESTAMP = get_current_timestamp()
CONFIG_DIR= 'config'
CONFIG_FILE_NAME= 'config.yaml'
CONFIG_FILE_PATH= os.path.join(
    ROOT_DIR,
    CONFIG_DIR,
    CONFIG_FILE_NAME
)



# Constants for Logger
LOG_DIR= 'logs'


# Constants for Training Pipeline
TRAINING_PIPLINE_CONFIG_KEY= 'training_pipeline_config'
PIPELINE_NAME_KEY= 'pipeline_name'
TRAINING_ARTIFACT_DIR_KEY= 'training_artifact_dir'


# Constants for Data Ingestion
DATA_INGESTION_CONFIG_KEY= 'data_ingestion_config'
DATA_INGESTION_DOWNLOAD_DATA_URL_KEY= 'download_data_url'
DATA_INGESTION_RAW_DATA_DIR_KEY= 'raw_data_dir'
DATA_INGESTION_INGESTED_DATA_DIR_KEY= 'ingested_data_dir'
DATA_INGESTION_INGESTED_TRAIN_DIR_KEY= 'ingested_train_dir'
DATA_INGESTION_INGESTED_TEST_DIR_KEY= 'ingested_test_dir'
DATA_INGESTION_ARTIFACT_DIR= 'data_ingestion'


# Constants for Schema File
SCHEMA_FILE_NAME= 'schema.yaml'
SCHEMA_FILE_PATH= os.path.join(
    ROOT_DIR,
    CONFIG_DIR,
    SCHEMA_FILE_NAME
)

SCHEMA_FILE_DATA_FILENAME= 'data_filename'
HISTORY_REPORT_DIR= 'history_report'

SCHEMA_FILE_FEATURES_KEY= 'features'
SCHEMA_FILE_LABEL_KEY= 'label'
SCHEMA_FILE_CONTINUOUS_FEATURES_KEY= 'continuous_features'
SCHEMA_FILE_DISCRETE_FEATURES_KEY= 'discrete_features'
SCHEMA_FILE_CATEGORICAL_FEATURES_KEY= 'categorical'
SCHEMA_FILE_DOMAIN_VALUES_KEY= 'domain_values'
LABEL_COLUMN= 'Response'


# Constants for Data Validation
DATA_VALIDATION_CONFIG_KEY= 'data_validation_config'
DATA_VALIDATION_ARTIFACT_DIR= 'data_validation'
DATA_VALIDATION_SCHEMA_FILE_DIR= 'schema_file_dir'
DATA_VALIDATION_SCHEMA_FILE_PATH= 'schema_file_path'
DATA_VALIDATION_REPORT_FILE_PATH= 'report_file_path'
DATA_VALIDATION_REPORT_PAGE_FILE_PATH= 'report_page_file_path'
EVIDENTLY_DATA_DRIFT_KEY= 'data_drift'
EVIDENTLY_METRICS_KEY= 'metrics'
EVIDENTLY_DATA_KEY= 'data'
EVIDENTLY_DATASET_DRIFT_KEY= 'dataset_drift'


# # Constants for Data Transformation
# DATA_TRANSFORMATION_CONFIG_KEY= 'data_transformation_config'
# DATA_TRANSFORMATION_ARTIFACT_DIR= 'data_transformation'
# DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR_KEY= 'transformed_data_dir'
# DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY= 'transformed_train_dir'
# DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY= 'transformed_test_dir'
# DATA_TRANSFORMATION_TRANSFORMED_PREPROCESSED_DIR_KEY= 'preprocessed_dir'
# DATA_TRANSFORMATION_TRANSFORMED_PREPROCESSED_MODEL_FILENAME_KEY= 'preprocessed_model_object_file_name'


