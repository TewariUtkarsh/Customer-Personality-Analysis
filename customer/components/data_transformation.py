import os, sys
from typing import List
import numpy as np
import pandas as pd
from datetime import datetime
from operator import concat
from customer.exception import CustomerException
from customer.logger import logging
from customer.entity.config_entity import DataTransformationConfig
from customer.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from customer.utils.util import csv_to_df, read_yaml_file, save_numpy_data, save_model_object
from customer.constants import *
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
# from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.decomposition import PCA
from kneed import KneeLocator


COLUMN_ID= 'ID'
COLUMN_Z_COST_CONTACT= 'Z_CostContact'
COLUMN_Z_REVENUE= 'Z_Revenue'
COLUMN_YEAR_BIRTH= 'Year_Birth'
COLUMN_DT_CUSTOMER= 'Dt_Customer'
COLUMN_DAY= 'd'
COLUMN_MONTH= 'm'
COLUMN_YEAR= 'y'



class FeatureEngineering(BaseEstimator, TransformerMixin):
    def __init__(self,
        column_ID_ix:int=0,
        column_Z_CostContact_ix:int=26,
        column_Z_Revenue_ix:int=27,
        column_Year_Birth_ix:int= 1,
        column_Dt_Customer_ix:int=7,
        columns:List= None
    ) -> None:
        # drop id, z_cols
        # year_birth -> age
        # dt_cust-> d,m,y
        
        self.columns= columns
        if self.columns is not None:
            column_ID_ix=self.columns.index(COLUMN_ID)
            column_Z_CostContact_ix= self.columns.index(COLUMN_Z_COST_CONTACT)
            column_Z_Revenue_ix= self.columns.index(COLUMN_Z_REVENUE)
            column_Year_Birth_ix= self.columns.index(COLUMN_YEAR_BIRTH)
            column_Dt_Customer_ix= self.columns.index(COLUMN_DT_CUSTOMER)
        self.column_ID_ix= column_ID_ix
        self.column_Z_CostContact_ix= column_Z_CostContact_ix
        self.column_Z_Revenue_ix= column_Z_Revenue_ix
        self.column_Year_Birth_ix= column_Year_Birth_ix
        self.column_Dt_Customer_ix= column_Dt_Customer_ix
        

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
    
        df= X.copy()
        # columns= list(df.columns)

        # Dropping Unecessary columns
        # df.drop(columns= [COLUMN_ID, COLUMN_Z_COST_CONTACT, COLUMN_Z_REVENUE], inplace=True)
        df.drop(columns= ['ID', 'Z_CostContact', 'Z_Revenue'], inplace=True)

        # Converting Year_Birth to age
        current_year= datetime.now().year
        df.iloc[:, self.column_Year_Birth_ix]= current_year - df.iloc[:, self.column_Year_Birth_ix]
        
        # Converting Dt_Customer to d,m,y
        df['y']= pd.to_datetime(df.iloc[:, self.column_Dt_Customer_ix]).dt.year
        df['m']= pd.to_datetime(df.iloc[:, self.column_Dt_Customer_ix]).dt.month
        df['d']= pd.to_datetime(df.iloc[:, self.column_Dt_Customer_ix]).dt.day

        df.drop(columns=['Dt_Customer'], inplace=True)

        return df
        

class CustomEncoder(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        self.column_data= {
            'Education':
            {
                'Graduation':5,
                'PhD':4,            
                'Master':3,         
                '2n Cycle':2,
                'Basic':1
            },
            'Marital_Status':
            {
                'Married':8,
                'Together':7,  
                'Single':6, 
                'Divorced':5,
                'Widow':4,
                'Alone':3,
                'Absurd':2,
                'YOLO':1
            }
        }

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        df= pd.DataFrame(X)
        df.columns= ['Education', 'Marital_Status']
        columns= df.columns
        for column in columns:
            df[column]= df[column].apply(lambda x: self.column_data[column][x])
        
        return df



class DimensionalityReduction(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        df= X.copy()
        pca= PCA()
        pca.fit(df)
        evr= pca.explained_variance_ratio_
        
        knee_locator= KneeLocator(range(df.shape[1]), np.cumsum(evr), direction='increasing', curve='concave')
        number_of_pcs= knee_locator.knee
        
        pca= PCA(n_components=number_of_pcs)
        transformed_df= pca.fit_transform(df)

        return transformed_df
        
    

class DataTransformation:
    def __init__(self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_artifact:DataValidationArtifact,
        data_transformation_config: DataTransformationConfig
    ) -> None:
        try:
            self.data_ingestion_artifact= data_ingestion_artifact
            self.data_validation_artifact= data_validation_artifact
            self.data_transformation_config= data_transformation_config
            self.schema_file_content= read_yaml_file(data_validation_artifact.schema_file_path)
        except Exception as e:
            raise CustomerException(e, sys) from e

    
    def get_preprocessed_model_object(self):
        try:
            continuous_columns= self.schema_file_content[SCHEMA_FILE_CONTINUOUS_FEATURES_KEY]
            discrete_columns= self.schema_file_content[SCHEMA_FILE_DISCRETE_FEATURES_KEY]

            numerical_columns= concat(continuous_columns, discrete_columns)

            categorical_columns= self.schema_file_content[SCHEMA_FILE_CATEGORICAL_FEATURES_KEY]

            final_columns= concat(numerical_columns, categorical_columns)

            new_final_columns= final_columns

            columns_to_be_removed= [COLUMN_ID, COLUMN_Z_COST_CONTACT, COLUMN_Z_REVENUE, COLUMN_DT_CUSTOMER]
            columns_to_be_added= [COLUMN_DAY, COLUMN_MONTH, COLUMN_YEAR]

            res= [new_final_columns.remove(column) for column in columns_to_be_removed]

            new_final_columns.extend(columns_to_be_added)
    
            numerical_pipeline= Pipeline(steps=[
                ('FeatureEngineering', FeatureEngineering()),
                ('impute', SimpleImputer(strategy='median')),
                # ('scaler', StandardScaler())
            ])

            categorical_pipeline= Pipeline(steps=[
                ('impute',SimpleImputer(strategy='most_frequent')),
                ('label_encoder', CustomEncoder()),
                # ('scaler', StandardScaler(with_mean=False, with_std=False))
            ])

            preprocessing= ColumnTransformer(transformers=[
                ('numerical_pipeline', numerical_pipeline, numerical_columns),
                ('categorical_pipeline', categorical_pipeline, categorical_columns)
            ])

            preprocessing_model_object=Pipeline(steps=[
                ('preprocessing', preprocessing),
                ('DimensionalityReduction', DimensionalityReduction())
            ])

            return preprocessing_model_object
        except Exception as e:
            raise CustomerException(e, sys) from e


    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            train_data_filepath= self.data_ingestion_artifact.train_data_filepath 
            test_data_filepath= self.data_ingestion_artifact.test_data_filepath

            train_df= csv_to_df(filepath=train_data_filepath)
            test_df= csv_to_df(filepath=test_data_filepath)

            label_column= LABEL_COLUMN
            x_train_data= train_df.drop(columns=[label_column])
            y_train_data= train_df[label_column]

            x_test_data= test_df.drop(columns=[label_column])
            y_test_data= test_df[label_column]

            preprocessed_model_object= self.get_preprocessed_model_object()


            transformed_x_train= preprocessed_model_object.fit_transform(X=x_train_data)
            transformed_x_test= preprocessed_model_object.transform(x_test_data)

            transformed_train_data= np.c_[transformed_x_train, y_train_data]
            transformed_test_data= np.c_[transformed_x_test, y_test_data]

            transformed_train_dir= self.data_transformation_config.transformed_train_dir
            train_data_filename= os.path.basename(train_data_filepath).replace('.csv','.npy')
            transformed_train_file_path= os.path.join(
                transformed_train_dir,
                train_data_filename
            )

            transformed_test_dir= self.data_transformation_config.transformed_test_dir
            test_data_filename= os.path.basename(test_data_filepath).replace('.csv','.npy')
            transformed_test_file_path= os.path.join(
                transformed_test_dir,
                test_data_filename
            )

            save_numpy_data(filepath=transformed_train_file_path, data=transformed_train_data)
            save_numpy_data(filepath=transformed_test_file_path, data=transformed_test_data)

            preprocessed_model_object_file_path= self.data_transformation_config.preprocessed_model_object_file_path

            save_model_object(filepath= preprocessed_model_object_file_path, model_object= preprocessed_model_object)

            data_transformation_artifact= DataTransformationArtifact(
                is_transformed=True,
                message='Data Transformation completed successfully.',
                transformed_train_file_path=transformed_train_file_path,
                transformed_test_file_path=transformed_test_file_path,
                preprocessed_model_object_file_path=preprocessed_model_object_file_path
            )

            return data_transformation_artifact

        except Exception as e:
            raise CustomerException(e, sys) from e




