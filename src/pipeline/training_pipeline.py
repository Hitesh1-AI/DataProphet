import os
import sys
import pandas as pd
import numpy as np

from dataclasses import dataclass

from src.components.data_validation import DataValidation
from src.components.data_ingestion import DataIngestion
from src.components.data_transform import DataTransform
from src.components.model_trainer import ModelTrainer
from src.components.clf_model_trainer import ClfModelTrainer
from src.Exception import CustomException
from src.logger import logging

class TrainingPipeline:
    def __init__(self):
        pass
    def train_models(self, data_file_path, problem):
        try:
            logging.info("Entered in Training Pipeline")
            obj = DataValidation()
            path = obj.initiate_data_validation(data_file_path)
            obj1 = DataIngestion()
            train_path , test_path = obj1.initiate_data_ingestion(path)

            obj2 = DataTransform()
            train, test , _ = obj2.initate_data_transformation(train_path, test_path)
            # print("train : ", train)
            # print("-----------------------------")
            # print('test : ', test)
            print("Model is Training...")
            if (problem == 'regresion'):
                model_trainer = ModelTrainer()
                score = model_trainer.initiate_model_trainer(train, test)
                return score
            else:
                # model_trainer = ClfModelTrainer()
                # score = model_trainer.initiate_classification_training(train, test)
                # return score
                print('yeah its working')
                logging.info('classification api call working!!')
        
        except Exception as e:
            raise CustomException(e, sys)