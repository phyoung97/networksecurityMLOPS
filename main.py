from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)
from networksecurity.components.model_trainer import ModelTrainer
import sys

if __name__ == '__main__':
    try:
        # --- Training pipeline config root ---
        trainingpipelineconfig = TrainingPipelineConfig()

        # --- Data Ingestion ---
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate Data Ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")
        print(dataingestionartifact)

        # --- Data Validation ---
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logging.info("Initiate Data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation completed")
        print(data_validation_artifact)

        # --- Data Transformation  ---
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        logging.info("Data Transformation started")
        data_transformation = DataTransformation(
            config=data_transformation_config,
            data_ingestion_artifact=dataingestionartifact,
            data_validation_artifact=data_validation_artifact,
        )
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Data Transformation complete")

        # --- Model Training ---
        logging.info("Model Training Started")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiant_model_trainer()
        logging.info("Model Training artifact created")

    except Exception as e:
        raise NetworkSecurityException(e, sys)