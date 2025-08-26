import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (DataTransformationArtifact,
                                                     DataValidationArtifact,
                                                     DataIngestionAtrifact)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils.utils import save_numpy_array, save_object


class DataTransformation:
    def __init__(
        self,
        config: DataTransformationConfig,
        data_validation_artifact: DataValidationArtifact,
        data_ingestion_artifact: DataIngestionAtrifact,
    ):
        try:
            self.config = config
            self.data_validation_artifact = data_validation_artifact
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    def get_data_transformer_object(self)-> Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a pipeline object with the KNNImputer object as the first step.

        Args:
        cls: DataTransformation

        Returns:
            A Pipeline object
        """
        logging.info(
            "Entered get_data_transformer object method od Transformation class"
        )
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def initiate_data_transformation(self) ->DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformation")

            if self.data_validation_artifact is None:
                raise ValueError(
                    "data_validation_artifact is None. Ensure DataValidation returns it and main.py passes it in."
                )

            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## Training Dataframe
            input_feature_train_df= train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df= train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            ## Testing Dataframe
            input_feature_test_df= test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df= test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_data_transformer_object()

            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

           # FIX: save to paths from self.config (not self.data_transformation_config)
            save_numpy_array(self.config.transformed_train_file_path, array=train_arr)   # FIX
            save_numpy_array(self.config.transformed_test_file_path, array=test_arr)     # FIX
            save_object(self.config.transformed_object_file_path, preprocessor_object)   # FIX

            # Save model pkl file into the final model folder

            save_object("final_model/preprocessor.pkl", preprocessor_object)


            # Prepare and RETURN artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.config.transformed_object_file_path,   # FIX
                transformed_train_file_path=self.config.transformed_train_file_path,     # FIX
                transformed_test_file_path=self.config.transformed_test_file_path,       # FIX
            )
            logging.info(f"DataTransformationArtifact: {data_transformation_artifact}")

            return data_transformation_artifact   # FIX: return it




        except Exception as e:
            raise NetworkSecurityException(e,sys)