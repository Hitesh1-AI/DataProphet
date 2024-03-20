from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import numpy as np
from typing import List

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import pandas as pd
import os,sys,time

from src.Exception import CustomException
from src.pipeline.training_pipeline import TrainingPipeline
from src.logger import logging

data_file_path = ''

app = FastAPI()

app.mount('/static', StaticFiles(directory="static"), name= "static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(requests: Request):
    return templates.TemplateResponse('index.html', {'request': requests})

@app.get("/home")
async def read_home(requests: Request):
    return templates.TemplateResponse('home.html', {'request': requests})

@app.get("/visualize")
async def visualize_data(requests: Request):
    return templates.TemplateResponse('visualize.html', {'request': requests})

@app.post("/uploaded", response_class= HTMLResponse)
async def upload_csv(requests: Request,csv_file: UploadFile = File(...)):
# async def upload_csv(csv_file: UploadFile = File(...), target : str = Form(...)):
    try:
        print('api is strated')
        logging.info("Api is starts working")
        contents = await csv_file.read()
        filename = csv_file.filename
        global data_file_path
        # if csv_file.content_type != 'application/csv':
        #     raise Exception("File is not of the correct content type")
        data_dir = os.path.join('artifacts', 'data') # logging.info("Move to training pipeline")
    
        os.makedirs(data_dir, exist_ok=True)
        data_file_path = os.path.join(data_dir, filename)
        
        with open(data_file_path, 'wb') as file:
            file.write(contents)
        print('file uploaded successfully')
        # return HTMLResponse('dashboard.html')
        # return f'File saved successfully'
        # redirect_url = "visualize.html"
        # return RedirectResponse(url = '/visualize') #to redirect the new page after uploading the form data
        logging.info("Move to training pipeline")
        
        # problem = 'regresion'
        # train_pipeline = TrainingPipeline()
        # score = train_pipeline.train_models(data_file_path, problem)

        # return score.tolist()
    
    except Exception as e:
        raise CustomException(e, sys)
    
@app.get("/training", response_class=HTMLResponse)
async def train(requests: Request):
    print('training api is called')
    problem = 'regresion'
    train_pipeline = TrainingPipeline()
    score = train_pipeline.train_models("artifacts/data/data_csv", problem)
    # return score.tolist()
    # return templates.TemplateResponse('visualize.html', {'request': requests})
    # score = 90
    return f"<h1>Training Complete</h1><p>Score: {score}</p>"

@app.get("/start-training",response_class= HTMLResponse)
async def start_training():
    # In this example, we will just return a simple HTML response with JavaScript
    return """
    <html>
<head>
    <title>Start Training</title>
    <style>
        #spinner {
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-left-color: #333;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: auto;
            position: absolute;
            top: 0; bottom: 0; left: 0; right: 0;
        }
        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
    </style>
</head>
<body>
    <div id="spinner"></div>
    <div id="result"></div>
    <script>
        async function startTraining() {
            const spinner = document.getElementById('spinner');
            spinner.style.display = 'block';  // Show the spinner
            
            const response = await fetch('/training', {
                method: 'GET',
            });
            const result = await response.text();
            document.getElementById('result').innerHTML = result;
            
            spinner.style.display = 'none';  // Hide the spinner once training is complete
        }
        startTraining();
    </script>
</body>
</html>
    """