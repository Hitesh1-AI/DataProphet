import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

from src.Exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_model
from sklearn.metrics import f1_score

@dataclass
class Classification_models_config:
    trained_classification_model_path = os.path.join('artifacts', 'clf_model.pkl')

class ClfModelTrainer:
    def __init__(self):
        self.classification_models_config = Classification_models_config()

    def initiate_classification_training(self, train_arr, test_arr):
        try:
            logging.info("Entered in Model Training")
            logging.info("Split the train and test Input data")
            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )
            models = {
                "Random Forest": RandomForestClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "SVM": SVC(),
                "LogisticRegression": LogisticRegression(),
                "KNeighborsClassifier": KNeighborsClassifier()
            }

            params = {
                "Random Forest":{
                    "n_estimators" : [10, 100, 1000],
                    "max_features" : ['sqrt', 'log2']
                },
                "Decision Tree":{
                    'max_depth':[3,5,7,10,15],
                    'min_samples_leaf':[3,5,10,15,20],
                    'min_samples_split':[8,10,12,18,20,16],
                    'criterion':['gini','entropy']
                },
                "Gradient Boosting": {
                    "n_estimators":[5,50,250,500],
                    "max_depth":[1,3,5,7,9],
                    "learning_rate":[0.01,0.1,1,10,100]
                },
                "SVM": {
                    'C': [0.1, 1, 10, 100, 1000],
                    'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
                    'kernel': ['rbf','linear']
              },
              "LogisticRegression":{
                  'solvers':['newton-cg', 'lbfgs', 'liblinear'],
                "penalty" : ['l2'],
                "c_values" : [100, 10, 1.0, 0.1, 0.01]
              },
              "KNeighborsClassifier":{
                  "n_neighbors" : range(1, 21, 2),
                    "weights": ['uniform', 'distance'],
                    "metric" : ['euclidean', 'manhattan', 'minkowski']
              }
            }
            model_report:dict= evaluate_model(X_train = X_train, y_train= y_train, X_test = X_test, y_test= y_test, models = models, param = params,metric=f1_score)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score< 0.6:
                raise CustomException("No best model found")
            
            logging.info("Best model found on both Test and Training data")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj= best_model
            )

            predicted = best_model.predict(X_test)

            score = f1_score(y_test, predicted)
            # print(score)
            metric = {'Model Name ':best_model_name,
                      'Model Accuracy': score}
            print(metric)
            return score          

        except CustomException as e:
            raise CustomException(sys, e)
