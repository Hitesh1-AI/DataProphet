import pandas as pd
import numpy as np
from src.Exception import CustomException
import sys

def data_validation(data, features):
    try:
        df = pd.read_csv(data)
        #first check for non datetime feature
        columns = [col for col in features if col not in ['date', 'Date']]
        count = 0
        for col in columns:
            count = df[col].nunique()
            if count > df.shape[0]*0.5 and df[col].dtype == 'O':
                df[col] = df[col].str.replace(",", "").astype(float)

    except Exception as e:
        raise CustomException(e, sys)
    
def save_object(file_path, obj):
    pass
   
