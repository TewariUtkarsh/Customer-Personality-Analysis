import os, sys
from customer.exception import CustomerException
from customer.logger import logging
from customer.entity.config_entity import DataValidationConfig
from customer.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact



class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact) -> None:
        try:
            self.data_validation_config= data_validation_config
            self.data_ingestion_artifact= data_ingestion_artifact
        except Exception as e: 
            raise CustomerException(e,sys) from e


    def is_data_present(self):
        try:
            pass
        except Exception as e: 
            raise CustomerException(e,sys) from e


    def is_colunm_validated(self):
        try:
            pass
        except Exception as e: 
            raise CustomerException(e,sys) from e


    # def 
        

    def is_data_drift_present(self):
        try:
            pass
        except Exception as e: 
            raise CustomerException(e,sys) from e


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            pass
        except Exception as e: 
            raise CustomerException(e,sys) from e