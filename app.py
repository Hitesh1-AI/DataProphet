from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import numpy as np
from typing import List

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import pandas as pd
import os,sys

from src.Exception import CustomException
from src.pipeline.training_pipeline import TrainingPipeline
from src.logger import logging

app = FastAPI()

app.mount('/static', StaticFiles(directory="static"), name= "static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(requests: Request):
    return templates.TemplateResponse('index.html', {'request': requests})


@app.post("/upload")
async def upload_csv(csv_file: UploadFile = File(...), target : str = Form(...)):
    # try:
    #     contents = await csv_file.read()
    #     filename = csv_file.filename
    #     return {"message": "File uploaded successfully", "filename": filename}
    # except Exception as e:
    #     return {"error": str(e)}
    try:
        logging.info("Api is starts working")
        contents = await csv_file.read()
        filename = csv_file.filename
        # if csv_file.content_type != 'application/csv':
        #     raise Exception("File is not of the correct content type")
        data_dir = os.path.join('artifacts', 'data') # logging.info("Move to training pipeline")
    
        os.makedirs(data_dir, exist_ok=True)
        data_file_path = os.path.join(data_dir, filename)
        
        with open(data_file_path, 'wb') as file:
            file.write(contents)
        
        # return f'File saved successfully and target variable is : {target}'
        # redirect_url = "home.html"
        # return RedirectResponse(url = redirect_url) #to redirect the new page after uploading the form data
        # logging.info("Move to training pipeline")
    
        # train_pipeline = TrainingPipeline()
        # score = train_pipeline.train_models(data_file_path, problem)
        # return score.tolist()
    
    except Exception as e:
        raise CustomException(e, sys)
    
