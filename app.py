from fastapi import FastAPI, UploadFile, File, Request
from pydantic import BaseModel
import numpy as np
from typing import List

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import os,sys

from src.Exception import CustomException
from src.pipeline.training_pipeline import TrainingPipeline
from src.logger import logging

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(requests: Request):
    return templates.TemplateResponse('index.html', {'request': requests})


@app.post("/upload")
async def upload_csv(csv_file: UploadFile = File(...)):
    # try:
    #     contents = await csv_file.read()
    #     filename = csv_file.filename
    #     return {"message": "File uploaded successfully", "filename": filename}
    # except Exception as e:
    #     return {"error": str(e)}
    try:
        logging.info("Api is starts working")
        contents = await csv_file.read()
        # if csv_file.content_type != 'application/csv':
        #     raise Exception("File is not of the correct content type")
        data_dir = os.path.join('artifacts', 'data')
        os.makedirs(data_dir, exist_ok=True)
        data_file_path = os.path.join(data_dir, 'new_data.csv')
        
        with open(data_file_path, 'wb') as file:
            file.write(contents)
        
        # return 'File saved successfully'
        
        logging.info("Move to training pipeline")
    
        train_pipeline = TrainingPipeline()
        score = train_pipeline.train_models(data_file_path)
        return score
    
    except Exception as e:
        raise CustomException(e, sys)
    
