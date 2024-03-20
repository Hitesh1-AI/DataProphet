import numpy as np
import pandas as pd
import os
import sys
import json

from src.Exception import CustomException
from src.logger import logging
from dataclasses import dataclass

@dataclass
class DataVisualizationConfig:
    visualization_data_path : str = os.path.join("artifacts", "visualize_data.json")

class DataVisualization:
    def __init__(self):
        self.data_visualizaton_config = DataVisualizationConfig()
        self.Is_Null = pd.Series
        self.data_types = pd.Series

    def get_visualization(self):
        try:
            df = pd.read_csv("artifacts/data/POP.csv")
            self.Is_Null = df.isnull().sum()
            self.data_types = df.dtypes
            # print(df.isnull().sum())
            # print(df.describe(include='all'))
            p = df.describe()
            # print(p['value']['mean'])
            return self.Is_Null
        
        except Exception as e:
            raise CustomException(e, sys)
    
if __name__== "__main__":
    obj = DataVisualization()
    obj.get_visualization()