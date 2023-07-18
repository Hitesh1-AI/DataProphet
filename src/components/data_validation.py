import os,sys
import pandas as pd
import numpy as np
from src.Exception import CustomException
from src.logger import logging

from dataclasses import dataclass

from src.components.data_ingestion import DataIngestion
from src.components.data_transform import DataTransform
from src.components.model_trainer import ModelTrainer

@dataclass
class DataValidationConfig:
    row_data_path :str = os.path.join('artifacts', 'row_data')
    # test_path : str = os.path.join('artifacts', 'test_data') 

class DataValidation:
    def __init__(self):
        self.data_validation_config = DataValidationConfig()

    def get_data_validation(self, df):
        try:
            #first check for non datetime feature
            columns = [col for col in df.columns if col not in ['date', 'Date']]
            count = 0
            for col in columns:
                count = df[col].nunique()
                if count > df.shape[0]*0.5 and df[col].dtype == 'O':
                    df[col] = df[col].str.replace(",", "").astype(float)
            
            #remove the id column as they are not an important for model
            for col in columns:
                if df[col].nunique() == df.shape[0] and df[col].max() == df.shape[0]:
                    columns.remove(col)

            return df[columns]
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self, data_file_path):
        try:
            logging.info("Entered in Data Validation")
            # df = pd.read_csv('src/notebook/DailyDelhiClimateTest.csv')
            df = pd.read_csv(data_file_path)
            logging.info("Start the Data Validation")
            data = self.get_data_validation(df)

            logging.info("Read the dataset to Dataframe")
            os.makedirs(os.path.dirname(self.data_validation_config.row_data_path),exist_ok=True)
            data.to_csv(self.data_validation_config.row_data_path, header=True, index=False)
            # print(data.columns)
            # print(data.info())
            logging.info("Data Validation is completed!!")
            logging.info("Validated Data is stored.")

            return (
                self.data_validation_config.row_data_path
            )
        
        except Exception as e:
            raise CustomException(e, sys)
        

# if __name__ == '__main__':
#     obj = DataValidation()
#     path = obj.initiate_data_validation()
#     obj1 = DataIngestion()
#     train_path , test_path = obj1.initiate_data_ingestion(path)

#     obj2 = DataTransform()
#     train, test , _ = obj2.initate_data_transformation(train_path, test_path)
#     # print("train : ", train)
#     # print("-----------------------------")
#     # print('test : ', test)
#     print("Model is Training...")
#     model_trainer = ModelTrainer()
#     model_trainer.initiate_model_trainer(train, test)