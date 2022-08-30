import os, sys
from customer.exception import CustomerException
from customer.logger import logging
from customer.config.configuration import Configuration
from customer.components.data_ingestion import DataIngestion
from customer.entity.config_entity import DataIngestionConfig
from customer.entity.artifact_entity import DataIngestionArtifact


class Pipeline:
    def __init__(self) -> None:
        try:
            config_object = Configuration()
            self.data_ingestion_config:DataIngestionConfig= config_object.get_data_ingestion_configuration()
        except Exception as e:
            raise CustomerException(e, sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:            
            data_ingestion= DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact= data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise CustomerException(e, sys) from e

    
    def run_pipeline(self):
        try:
            data_ingestion_artifact= self.start_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise CustomerException(e, sys) from e


    # def __del__(self) -> None:
    #     pass
