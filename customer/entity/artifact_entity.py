from collections import namedtuple


# Data Ingestion Artifact
DataIngestionArtifact= namedtuple('DataIngestionArtifact',
['is_ingested', 'message', 'train_data_filepath','test_data_filepath'])


# Data Validation Artifact
DataValidationArtifact= namedtuple('DataValidationArtifact',
['is_validated','message', 'report_file_path' ,'report_page_file_path','schema_file_path'])


# Data Transformation Artifact
DataTransformationArtifact= namedtuple('DataTransformationArtifact',
['is_transformed', 'message', 'transformed_train_file_path', 'transformed_test_file_path', 'preprocessed_model_object_file_path'])

