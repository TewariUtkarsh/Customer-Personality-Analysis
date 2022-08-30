import os
import sys
from customer.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from customer.constants import *
from customer.exception import CustomerException
from customer.logger import logging
from customer.utils.util import read_yaml_file



class Configuration:

    def __init__(self, config_file_path:str=CONFIG_FILE_PATH, current_timestamp:str=CURRENT_TIMESTAMP) -> None:
        try:
            self.config_file_path= config_file_path
            self.current_timestamp= current_timestamp
            self.config_file_info= read_yaml_file(filepath= self.config_file_path)
            self.training_pipeline_config= self.get_training_pipeline_configuration()
        except Exception as e:
            raise CustomerException(e, sys) from e


    def get_training_pipeline_configuration(self) -> TrainingPipelineConfig:
        try:
            training_pipeline_config_info= self.config_file_info[TRAINING_PIPLINE_CONFIG_KEY]
            training_artifact_dir= os.path.join(
                ROOT_DIR,
                training_pipeline_config_info[PIPELINE_NAME_KEY],
                training_pipeline_config_info[TRAINING_ARTIFACT_DIR_KEY]
            )

            training_pipeline_config= TrainingPipelineConfig(
                training_artifact_dir= training_artifact_dir
            )
            
            return training_pipeline_config
        except Exception as e:
            raise CustomerException(e, sys) from e


    def get_data_ingestion_configuration(self) -> DataIngestionConfig:
        try:
            data_ingestion_config_info= self.config_file_info[DATA_INGESTION_CONFIG_KEY]

            data_ingestion_artifact_dir= os.path.join(
                self.training_pipeline_config.training_artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                CURRENT_TIMESTAMP
            )

            download_data_url= data_ingestion_config_info[DATA_INGESTION_DOWNLOAD_DATA_URL_KEY]
            
            raw_data_dir= os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_config_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )

            ingested_data_dir= os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_config_info[DATA_INGESTION_INGESTED_DATA_DIR_KEY]
            )
            
            ingested_train_dir= os.path.join(
                ingested_data_dir,
                data_ingestion_config_info[DATA_INGESTION_INGESTED_TRAIN_DIR_KEY]
            )

            ingested_test_dir= os.path.join(
                ingested_data_dir,
                data_ingestion_config_info[DATA_INGESTION_INGESTED_TEST_DIR_KEY]
            )
            

            data_ingestion_config = DataIngestionConfig(
                download_data_url= download_data_url,
                raw_data_dir= raw_data_dir,
                ingested_train_dir= ingested_train_dir,
                ingested_test_dir= ingested_test_dir
            )

            return data_ingestion_config
        except Exception as e:
            raise CustomerException(e, sys) from e

    

    # def get_data_validation_configuration(self) -> DataValidationConfig:
    #     try:
    #         data_validation_config_info= self.config_file_info[DATA_VALIDATION_CONFIG_KEY]

    #         data_validation_artifact_dir= os.path.join(
    #             self.training_pipeline_config.training_artifact_dir,
    #             DATA_VALIDATION_ARTIFACT_DIR,
    #             self.current_timestamp
    #         )

    #         schema_file_path= os.path.join(
    #             data_validation_artifact_dir,
    #             data_validation_config_info[DATA_VALIDATION_SCHEMA_FILE_PATH_KEY]
    #         )

    #         report_file_path= os.path.join(
    #             data_validation_artifact_dir,
    #             data_validation_config_info[DATA_VALIDATION_REPORT_FILE_KEY]
    #         )
            
    #         report_page_file_path= os.path.join(
    #             data_validation_artifact_dir,
    #             data_validation_config_info[DATA_VALIDATION_REPORT_PAGE_FILE_KEY]
    #         )

    #         data_validation_config= DataValidationConfig(
    #             schema_file_path=schema_file_path,
    #             report_file_path=report_file_path,
    #             report_page_file_path=report_page_file_path
    #         )

    #         return data_validation_config

    #     except Exception as e:
    #         raise CustomerException(e, sys) from e
