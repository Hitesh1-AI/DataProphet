import os, sys
from src.Exception import CustomException
from src.logger import logging

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer


from src.utils import save_object

from dataclasses import dataclass

import pandas as pd
import numpy as np

@dataclass
class DataTransformConfig:
    preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransform:
    def __init__(self):
        self.data_transform_config = DataTransformConfig()
    def get_data_transform(self, num_col, cat_col):
        try:
            num_features = num_col
            cat_features = cat_col

            num_pipeline = Pipeline(
                steps=[
                    ( 'Imputer',SimpleImputer(strategy='mean')),
                    ('Normalization', StandardScaler())
                     
                ]
            )
            preprocessor = ColumnTransformer(
                [
                ('num_pipeline', num_pipeline, num_features)
                ]
            )

            if cat_features:
                print(cat_features)
                print('it still working-------------------------------------------------')
                cat_pipeline = Pipeline(
                    steps=[
                        
                        ('Imputer', SimpleImputer(strategy='most_frequent')),
                        ('OneHotEncode', OneHotEncoder(categories='auto', handle_unknown=True)),
                        ('Normalization', StandardScaler())
                            
                    ]
                )

                preprocessor = ColumnTransformer(
                    [
                    ('num_pipeline', num_pipeline, num_features),
                    ('cat_pipeline', cat_pipeline, cat_features)
                    ]
                )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)

    def initate_data_transformation(self, train_path, test_path):
        try:
            logging.info("Entered the Data Transform Method")
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)
            target_col = 'meantemp'

            train_columns  = [col for col in train_data.columns if col not in 
                                    ['Date', 'date', 'DATE']]
            test_columns =  [col for col in test_data.columns if col not in 
                                    ['Date', 'date', 'DATE']]
            
            # train_columns = [col for col in train_columns if col not in target_col]
            # test_columns = [col for col in train_columns if col not in target_col]
            
            cat_col = [col for col in train_columns if train_data[col].dtype == "O"]
            num_col = [col for col in train_columns if train_data[col].dtype != "O"]
            cat_col = [col for col in cat_col if col not in target_col]
            num_col = [col for col in num_col if col not in target_col]
            # print(train_columns)

            # print("catcol : ",cat_col)
            # print('numcol : ', num_col)
            logging.info("Creating the Preprocessor Object")
            preprocessor = self.get_data_transform(num_col, cat_col)

            
            train_input_df = train_data[train_columns].drop(target_col, axis=1)
            target_train_df = train_data[target_col]
            # print(train_input_df.columns)

            test_input_df = test_data[test_columns].drop(target_col, axis=1)
            target_test_df = test_data[target_col]

            train_input_arr = preprocessor.fit_transform(train_input_df)
            test_input_arr = preprocessor.transform(test_input_df)
            logging.info("Preprocessor object is created")
            # print(train_input_arr.shape)
            # print(train_input_arr.colu)
            train_arr = np.c_[train_input_arr, target_train_df]
            test_arr = np.c_[test_input_arr, target_test_df]

            print(train_arr[:5])
            # print(test_arr.shape)
            
            save_object(
                file_path = self.data_transform_config.preprocessor_path,
                obj = preprocessor
            )
            return (
                train_arr,
                test_arr,
                self.data_transform_config.preprocessor_path
            )


        except Exception as e:
            raise CustomException(e, sys)