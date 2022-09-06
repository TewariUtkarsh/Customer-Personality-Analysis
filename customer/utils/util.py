import os, sys
import yaml
import pandas as pd
import numpy as np
from customer.exception import CustomerException
from customer.logger import logging
import json
import dill, pickle


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
       data.to_csv(filepath, index=False)
    except Exception as e:
        raise CustomerException(e,sys) from e


def csv_to_df(filepath: str, sep:str=',') -> pd.DataFrame:
    try:
        df= pd.read_csv(filepath, sep=sep)
        return df
    except Exception as e:
        raise CustomerException(e, sys) from e


def save_json_file(obj:dict, filepath: str) -> None:
    try:
        with open(filepath, 'w') as f:
            json.dump(obj, f, indent=6)
    except Exception as e:
        raise CustomerException(e, sys ) from e


def save_numpy_data(filepath:str, data:np.array) -> None:
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as file_object:
            np.save(file_object, data)
    except Exception as e:
        raise CustomerException(e, sys) from e


def save_model_object(filepath:str, model_object) -> None:
    try:
        os.makedirs(os.path.dirname(filepath))
        with open(filepath, 'wb') as file_object:
            dill.dump(model_object, file_object)
    except Exception as e:
        raise CustomerException(e, sys) from e