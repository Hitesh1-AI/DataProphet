from src.Exception import CustomException
from src.logger import logging
import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

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
            df = pd.read_csv('notebook/data/data.csv')

            logging.info("Read the dataset to Dataframe")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, header=True, index=False)
            
            logging.info("Train test split the data")

            train_set, test_set = train_test_split(df, test_size = 0.2, random_state = 42, shuffle=True)
            train_set.to_csv(self.ingestion_config.train_data_path, index= False, header= True)
            test_set.to_csv(self.ingestion_config.test_data_path, index= False, header= True)
            
            logging.info("Data ingestion is complited")

            return(
                self.data_ingestion_config.train_path,
                self.data_ingestion_config.test_path
            )
        except Exception as e:
            raise CustomException(e, sys)