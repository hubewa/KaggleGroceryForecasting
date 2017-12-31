# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 23:24:34 2017

@author: Hubert
"""

import xgboost as xgb
import sklearn
import numpy as np

import datetime

import math

def trainXGModel(train):
    target = train['unit_sales']
    train['unit_sales'] = train['unit_sales'].astype('category')
    
    train = train.drop(['unit_sales'], axis=1)   
    
    currentTime = datetime.datetime.now().isoformat()
    print("Train time begin:", currentTime)
    xgModel = xgb.XGBRegressor().fit(train, target)
    finishTime = datetime.datetime.now().isoformat()
    print("Train time finish:", finishTime)
    return xgModel

def loss(prediction, values):
    subtract = np.subtract([np.log1p(x) for x in prediction], [np.log1p(x) for x in values])
    print("Subtract = ", subtract)
    loss = pow((np.sum(pow(x,2) for x in subtract)/prediction.size),0.5)
    print ("loss = ", loss)
    return loss