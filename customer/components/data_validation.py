from email import message
import json
import os, sys
from tkinter.tix import Tree
import pandas as pd
from typing import Dict, List
from customer.exception import CustomerException
from customer.logger import logging
from customer.entity.config_entity import DataValidationConfig
from customer.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
from customer.utils.util import save_json_file
from customer.utils.util import *
from customer.constants import *
from customer.config.configuration import Configuration




class DataValidation:

    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig) -> None:
        try:
            self.data_ingestion_artifact= data_ingestion_artifact
            self.data_validation_config= data_validation_config
        except Exception as e:
            raise CustomerException(e, sys) from e

    
    
    def is_data_present(self) -> bool:
        try:
            is_train_file_exist= False
            is_test_file_exist= False
            
            train_file_path= self.data_ingestion_artifact.train_data_filepath
            test_file_path= self.data_ingestion_artifact.test_data_filepath

            if os.path.exists(train_file_path):
                is_train_file_exist= True

            if os.path.exists(test_file_path):
                is_test_file_exist= True


            is_validated= is_train_file_exist and is_test_file_exist

            return is_validated
        except Exception as e:
            raise CustomerException(e, sys) from e


    def validate_file_name_ext(self) -> bool:
        try:
            is_validated= False
            schema_file_content= read_yaml_file(self.data_validation_config.schema_file_path)
            data_filename= schema_file_content[SCHEMA_FILE_DATA_FILENAME]

            train_data_filename= os.path.basename(self.data_ingestion_artifact.train_data_filepath)
            test_data_filename = os.path.basename(self.data_ingestion_artifact.test_data_filepath)

            if (train_data_filename==data_filename) and (test_data_filename==data_filename):
                is_validated= True


            return is_validated

        except Exception as e:
            raise CustomerException(e, sys) from e


    def is_columns_valid(self) -> bool:
        try:
            is_validated= False

            schema_file= read_yaml_file(filepath=self.data_validation_config.schema_file_path)            
            schema_file_columns= schema_file[SCHEMA_FILE_FEATURES_KEY]

            train_df= csv_to_df(self.data_ingestion_artifact.train_data_filepath)
            train_df_columns= list(train_df.columns)


            # num of cols same
            # name and dtype same
            # domain value same

            # train file
            
            if len(schema_file_columns)==len(train_df_columns):
                for name in schema_file_columns:
                    if train_df[name].dtype==schema_file_columns[name]:
                        is_validated=True
                    else:
                        is_validated=False
                        return is_validated

                schema_domain_values= schema_file[SCHEMA_FILE_DOMAIN_VALUES_KEY]
                for column in schema_domain_values:
                    schema_domain_set= set(schema_domain_values[column])
                    train_df_domain_set= set(train_df[column].unique())

                    if schema_domain_set.intersection(train_df_domain_set)==train_df_domain_set:
                        is_validated=True

                    else:
                        is_validated= False
                        return is_validated

                    
            else:
                is_validated=False
                return is_validated

            # test file

            test_df= csv_to_df(filepath=self.data_ingestion_artifact.test_data_filepath)
            test_df_columns= list(test_df.columns)

            if len(schema_file_columns)==len(test_df_columns):
                for col in schema_file_columns:
                    if test_df[col].dtype==schema_file_columns[col]:
                        is_validated= True
                    else:
                        is_validated= False
                        return is_validated
                for col in schema_domain_values:
                    test_df_domain_set= set(test_df[col].unique())
                    schema_domain_set= set(schema_domain_values[col])

                    if schema_domain_set.intersection(test_df_domain_set)==test_df_domain_set:
                        is_validated= True
                    else:
                        is_validated= False
                        return is_validated
            else:
                is_validated= False


            return is_validated

        except Exception as e:
            raise CustomerException(e, sys) from e


    
    def generate_and_save_report_file(self, reference_data: pd.DataFrame, current_data: pd.DataFrame) -> List:
        try:
            profile= Profile(sections=[DataDriftProfileSection()])
            profile.calculate(reference_data=reference_data, current_data=current_data)
            
            report_file_content= profile.json()
            report_file_content= json.loads(report_file_content)

            report_file_path= self.data_validation_config.report_file_path

            os.makedirs(os.path.dirname(report_file_path))

            save_json_file(obj=report_file_content, filepath=report_file_path)

            return [report_file_path,report_file_content]

        except Exception as e:
            raise CustomerException(e, sys) from e



    def generate_and_save_report_page(self,  reference_data: pd.DataFrame, current_data: pd.DataFrame) -> str:
        try:
            dashboard= Dashboard(tabs=[DataDriftTab()])
            dashboard.calculate(reference_data=reference_data,current_data=current_data)

            report_page_file_path= self.data_validation_config.report_page_file_path
            dashboard.save(report_page_file_path)


            return report_page_file_path

        except Exception as e:
            raise CustomerException(e, sys) from e



    def is_data_drift_present(self):
        try:
            data_drift=True
            
            train_df= csv_to_df(filepath=self.data_ingestion_artifact.train_data_filepath)
            test_df= csv_to_df(filepath=self.data_ingestion_artifact.test_data_filepath)

            report_file_path, report_file_content= self.generate_and_save_report_file(reference_data=train_df, current_data=test_df)
            data_drift= report_file_content[EVIDENTLY_DATA_DRIFT_KEY][EVIDENTLY_DATA_KEY][EVIDENTLY_METRICS_KEY][EVIDENTLY_DATASET_DRIFT_KEY]

            report_page_file_path= self.generate_and_save_report_page(reference_data=train_df, current_data=test_df)

            is_validated= not data_drift

            return [is_validated, report_file_path, report_page_file_path]

        except Exception as e:
            raise CustomerException(e, sys) from e



    def check_and_generate_history_report(self, record_type:str='recent') -> None:
        try:
            # 'recent' or 'oldeest'
            record_type= record_type

            # get old data both train and test
            # 1. data_ingestion_artifact, cd ..
            # 2. config()
            # 3. config.yaml
            ## 1. data_ingestion_dir= os.path.dirname(self.data_ingestion_artifact.train_data_filepath)

            ## 2. config= Configuration()

            ## 3. config.yaml

            ## 4. from cwd to ingested_data dir using chdir, string split

            config= Configuration()

            config_file_content= config.config_file_info

            training_pipeline_config= config.get_training_pipeline_configuration()
            training_artifact_dir= training_pipeline_config.training_artifact_dir



            data_ingestion_config_info= config_file_content[DATA_INGESTION_CONFIG_KEY]

            data_ingestion_artifact_dir= os.path.join(
                training_artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR
            )

            data_ingestion_artifacts= os.listdir(data_ingestion_artifact_dir)
            data_ingestion_artifacts.sort()

            if record_type=='recent':
                data_ingestion_artifact= data_ingestion_artifacts[-2]


            elif record_type=='oldest':
                data_ingestion_artifact= data_ingestion_artifacts[0]


            else:
                raise Exception('Invalid Input Provided.')


            # Checking for Data Drift upon Training Data
            
            train_data_dir= os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_artifact,
                data_ingestion_config_info[DATA_INGESTION_INGESTED_DATA_DIR_KEY],
                data_ingestion_config_info[DATA_INGESTION_INGESTED_TRAIN_DIR_KEY]
            )
            
            train_data_filename= os.listdir(train_data_dir)[0]

            train_data_file_path= os.path.join(
                train_data_dir,
                train_data_filename
            )

            reference_train_df= csv_to_df(filepath=train_data_file_path)

            current_train_df= csv_to_df(filepath=self.data_ingestion_artifact.train_data_filepath)

            train_profile= Profile(sections=[DataDriftProfileSection()])
            train_profile.calculate(reference_train_df, current_train_df)

            train_profile_content= train_profile.json()
            train_profile_content= json.loads(train_profile_content)

            data_validation_artifact_dir= os.path.dirname(self.data_validation_config.report_file_path)

            report_file_name= os.path.basename(self.data_validation_config.report_file_path)

            history_report_dir= os.path.join(
                data_validation_artifact_dir,
                HISTORY_REPORT_DIR
            )

            train_history_report_dir= os.path.join(
                history_report_dir,
                data_ingestion_config_info[DATA_INGESTION_INGESTED_TRAIN_DIR_KEY]
            )

            os.makedirs(train_history_report_dir, exist_ok=True)

            train_history_report_file_path= os.path.join(
                train_history_report_dir,
                report_file_name
            )

            save_json_file(obj=train_profile_content, filepath=train_history_report_file_path)

            train_dashboard= Dashboard(tabs=[DataDriftTab()])
            train_dashboard.calculate(reference_train_df, current_train_df)

            report_page_file_name= os.path.basename(self.data_validation_config.report_page_file_path)

            train_history_report_page_file_path= os.path.join(
                train_history_report_dir,
                report_page_file_name
            )

            train_dashboard.save(train_history_report_page_file_path)





            # Checking for Data Drift upon Testing Data

            test_data_dir= os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_artifact,
                data_ingestion_config_info[DATA_INGESTION_INGESTED_DATA_DIR_KEY],
                data_ingestion_config_info[DATA_INGESTION_INGESTED_TEST_DIR_KEY]
            )
            
            test_data_filename= os.listdir(test_data_dir)[0]

            test_data_file_path= os.path.join(
                test_data_dir,
                test_data_filename
            )

            reference_test_df= csv_to_df(filepath=test_data_file_path)

            current_test_df= csv_to_df(filepath=self.data_ingestion_artifact.test_data_filepath)

            test_profile= Profile(sections=[DataDriftProfileSection()])
            test_profile.calculate(reference_test_df, current_test_df)

            test_profile_content= test_profile.json()
            test_profile_content= json.loads(test_profile_content)

            data_validation_artifact_dir= os.path.dirname(self.data_validation_config.report_file_path)

            # report_file_name= os.path.basename(self.data_validation_config.report_file_path)
            
            test_history_report_dir= os.path.join(
                history_report_dir,
                data_ingestion_config_info[DATA_INGESTION_INGESTED_TEST_DIR_KEY]
            )
            os.makedirs(test_history_report_dir, exist_ok=True)
            test_history_report_file_path= os.path.join(
                test_history_report_dir,
                report_file_name
            )

            save_json_file(obj=test_profile_content, filepath=test_history_report_file_path)

            test_dashboard= Dashboard(tabs=[DataDriftTab()])
            test_dashboard.calculate(reference_test_df, current_test_df)

            # test_report_page_file_name= os.path.basename(self.data_validation_config.report_page_file_path)

            test_history_report_page_file_path= os.path.join(
                test_history_report_dir,
                report_page_file_name
            )

            test_dashboard.save(test_history_report_page_file_path)
            
            is_checked= True
            return is_checked
            


        except Exception as e:
            raise CustomerException(e, sys) from e  

            
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            is_validated= False
            report_file_path=''
            report_page_file_path=''
            message='Data is not validated. Inconsistency Detected.'
            is_validated= self.is_data_present()

            if is_validated==True:
                is_validated= self.validate_file_name_ext()

                if is_validated==True:
                    is_validated= self.is_columns_valid()

                    if is_validated==True:
                        is_validated, report_file_path, report_page_file_path= self.is_data_drift_present()
                        message='Data Validation completed successfully.'
            data_validation_artifact= DataValidationArtifact(
                is_validated= is_validated,
                message= message,
                report_file_path=report_file_path,
                report_page_file_path=report_page_file_path,
                schema_file_path=self.data_validation_config.schema_file_path
            )
            is_checked= self.check_and_generate_history_report(record_type='oldest')

            return data_validation_artifact

        except Exception as e:
            raise CustomerException(e, sys) from e
