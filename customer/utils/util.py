import os, sys
import yaml
import pandas as pd
from customer.exception import CustomerException
from customer.logger import logging


def read_yaml_file(filepath: str) -> dict:
    try:
        with open(filepath, 'r') as file_obj:
            yaml_content= yaml.safe_load(file_obj)
            return yaml_content
        
    except Exception as e:
        raise CustomerException(e,sys) from e


def read_csv_file(filepath: str, sep:str=',') -> pd.DataFrame:
    try:
        df= pd.read_csv(filepath, sep=sep)
        return df
        
    except Exception as e:
        raise CustomerException(e,sys) from e


def df_to_csv(filepath: str, data: pd.DataFrame):
    try:
       data.to_csv(filepath)
    except Exception as e:
        raise CustomerException(e,sys) from e