import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.grid_search import GridSearchCV

from sklearn.cluster import KMeans

class models(object):
    '''
    graphing
        dendrograms
        auc roc curves
        boundary curves for SVM
        mesh grids classification
    '''
    def __init__(self):
        params_ = params = {

                RandomForestClassifier():
            {
                'n_estimators':[200],
                'max_features': [8,9,10,11],
                'random_state': [1]
             },
                LogisticRegression():
            { 
                'penalty': ['l2'],
                'C' : [.01, 0.1, 1, 10],
                'random_state' : [1]
            },
                KNeighborsClassifier():
            {
                'n_neighbors' : [2, 5, 10, 50]
            },
                SVC():
            {
                'C': [.01, 0.1, 1, 10],
                'kernel': ['linear', 'rbf', 'poly'],
                'degree' : [2,3],
                'gamma' : [0, 0.01, 0.1, 0.5],
                'random_state' : [1]
            },
                GradientBoostingClassifier():
            {
                'learning_rate' : [0.01, 0.1, 0.5, 1],
                'n_estimators' : [50, 100, 200],
                'max_depth' : [2,3,4]
            }
        }

