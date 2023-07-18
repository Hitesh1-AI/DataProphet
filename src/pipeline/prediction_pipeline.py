import numpy as np
import pandas as pd
import os
import sys

from src.Exception import CustomException
from src.logger import logging
from src.utils import load_object

class PredictionPipeline:
    def __init__(self):
        pass
    def predict(self):
        df = pd.read_csv('artifacts/test_data.csv')
        model = load_object('artifacts/model.pkl')
        y_pred = model.predict(df[:, :-1]).tolist()
        return y_pred
    