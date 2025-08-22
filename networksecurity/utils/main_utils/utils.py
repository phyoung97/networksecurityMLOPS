import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
#import dill
import pickle

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    

def write_yaml_file(file_path: str,content:object,replace:bool=False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def save_numpy_array(file_path: str , array: np.array):
    """
    Save numpy array data to file
    file_path: str location of the file to save
    array: np.array data to save
    """

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    

def load_numpy_array(file_path: str):
    """
    Load a NumPy array from .npy or .npz.
    - For .npy: returns the array.
    - For .npz: returns the single array if only one is stored; otherwise a tuple of arrays.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"NumPy file not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".npy":
            # np.load on a file path returns the array directly
            return np.load(file_path, allow_pickle=False)
        elif ext == ".npz":
            with np.load(file_path, allow_pickle=False) as data:
                keys = list(data.keys())
                if len(keys) == 1:
                    return data[keys[0]]
                return tuple(data[k] for k in keys)
        else:
            raise ValueError(f"Unsupported file extension {ext}. Use .npy or .npz.")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    


def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Excited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    

def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs= GridSearchCV(model, para, cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = accuracy_score(y_train, y_train_pred)

            test_model_score = accuracy_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report
    except Exception as e:
        raise NetworkSecurityException(e,sys)