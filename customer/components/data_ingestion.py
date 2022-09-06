import os, sys
from typing import List
from six.moves import urllib
from sklearn.model_selection import StratifiedShuffleSplit
from customer.constants import *
from customer.exception import CustomerException
from customer.logger import logging
from customer.entity.config_entity import DataIngestionConfig
from customer.entity.artifact_entity import DataIngestionArtifact
from customer.utils.util import read_csv_file, df_to_csv


class DataIngestion:

    def __init__(self, data_ingestion_config:DataIngestionConfig) -> None:
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomerException(e, sys) from e


    # download to dest, extract, raw_data, test-train
    def download_data(self) -> str:
        try:
            download_data_url= self.data_ingestion_config.download_data_url
            
            download_data_filename= os.path.basename(download_data_url)
            
            raw_data_dir= self.data_ingestion_config.raw_data_dir
            os.makedirs(raw_data_dir, exist_ok=True)

            raw_data_filepath= os.path.join(
                raw_data_dir,
                download_data_filename
            )

            urllib.request.urlretrieve(download_data_url, raw_data_filepath)
            
            return raw_data_filepath

        except Exception as e:
            raise CustomerException(e, sys) from e



    def train_test_file_split(self, raw_data_filepath:str) -> List:
        try:
            
            raw_data_filename= os.path.basename(raw_data_filepath)

            data= read_csv_file(raw_data_filepath, sep=';')
    
            stratified= StratifiedShuffleSplit(n_splits=2, test_size=0.2, random_state=1)

            stratified_train = None 
            stratified_test = None

            for train_idx, test_idx in stratified.split(data, data[LABEL_COLUMN]):
                stratified_train= data.iloc[train_idx, :]
                stratified_test= data.iloc[test_idx, :]

            
            train_data_filepath= os.path.join(
                    self.data_ingestion_config.ingested_train_dir,
                    raw_data_filename
                )

            test_data_filepath= os.path.join(
                    self.data_ingestion_config.ingested_test_dir,
                    raw_data_filename
            )

            if stratified_train is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)

                df_to_csv(filepath=train_data_filepath, data=stratified_train)

            
            if stratified_test is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)

                df_to_csv(filepath=test_data_filepath, data=stratified_test)
            
            
            return [train_data_filepath, test_data_filepath]

            
        except Exception as e:
            raise CustomerException(e, sys) from e



    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            raw_data_filepath= self.download_data()
            train_data_filepath, test_data_filepath= self.train_test_file_split(raw_data_filepath=raw_data_filepath)
            message= 'Data Ingestion Completed Successfully.'
            data_ingestion_artifact= DataIngestionArtifact(
                is_ingested=True,
                message=message,
                train_data_filepath=train_data_filepath,
                test_data_filepath=test_data_filepath
            )
            return data_ingestion_artifact
        except Exception as e:
            raise CustomerException(e, sys) from e


    def __del__(self) -> None:
        pass
        