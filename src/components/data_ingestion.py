from src.Exception import CustomException
from src.logger import logging
import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transform import DataTransform

@dataclass
class DataIngestionConfig:
    train_path :str = os.path.join('artifacts', 'train_data')
    test_path : str = os.path.join('artifacts', 'test_data')
    row_data_path :str = os.path.join('artifacts', 'row_data')

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the Data Ingestion Method")
        try:
            df = pd.read_csv('src/notebook/DailyDelhiClimateTest.csv')

            logging.info("Read the dataset to Dataframe")
            os.makedirs(os.path.dirname(self.data_ingestion_config.train_path),exist_ok=True)
            df.to_csv(self.data_ingestion_config.row_data_path, header=True, index=False)
            
            logging.info("Train test split the data")

            train_set, test_set = train_test_split(df, test_size = 0.2, random_state = 42, shuffle=True)
            train_set.to_csv(self.data_ingestion_config.train_path, index= False, header= True)
            test_set.to_csv(self.data_ingestion_config.test_path, index= False, header= True)
            
            logging.info("Data ingestion is complited")

            return(
                self.data_ingestion_config.train_path,
                self.data_ingestion_config.test_path
            )
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__== '__main__':
    obj = DataIngestion()
    train_path , test_path = obj.initiate_data_ingestion()

    obj2 = DataTransform()
    obj2.initate_data_transformation(train_path, test_path)