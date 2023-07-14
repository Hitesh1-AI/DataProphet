import os, sys
from src.Exception import CustomException
from src.logger import logging

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

from dataclasses import dataclass

@dataclass
class DataTransformConfig:
    def __init__(self):
        self.preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransform:
    def __init__(self):
        self.data_transform_config = DataTransformConfig()
    def get_data_transform(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys)

