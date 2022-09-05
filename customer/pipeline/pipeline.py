import os, sys
from customer.exception import CustomerException
from customer.logger import logging
from customer.config.configuration import Configuration
from customer.components.data_ingestion import DataIngestion
from customer.components.data_validation import DataValidation
from customer.entity.config_entity import DataIngestionConfig, DataValidationConfig
from customer.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact


class Pipeline:
    def __init__(self) -> None:
        try:
            config_object = Configuration()
            self.data_ingestion_config:DataIngestionConfig= config_object.get_data_ingestion_configuration()
            self.data_validation_config:DataIngestionConfig= config_object.get_data_validation_configuration()
        except Exception as e:
            raise CustomerException(e, sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:            
            data_ingestion= DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact= data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise CustomerException(e, sys) from e

    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation= DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )


            data_validation_artifact= data_validation.initiate_data_validation()
            return data_validation_artifact

        except Exception as e:
            raise CustomerException(e, sys) from e


    def run_pipeline(self):
        try:
            data_ingestion_artifact= self.start_data_ingestion()
            data_validation_artifact= self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            return data_validation_artifact
        except Exception as e:
            raise CustomerException(e, sys) from e


    # def __del__(self) -> None:
    #     pass
