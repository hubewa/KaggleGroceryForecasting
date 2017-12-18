# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 23:24:34 2017

@author: Hubert
"""

import xgboost as xgb
import sklearn
import numpy as np

import math

def trainXGModel(train):
    target = train['unit_sales']
    train = train.drop(['unit_sales'], axis=1)   
    

    xgModel = xgb.XGBRegressor().fit(train, target)
    return xgModel

def loss(prediction, values):
    subtract = np.subtract([math.log1p(x) for x in prediction], [math.log1p(x) for x in values])
    print("Subtract = ", subtract)
    loss = pow((np.sum(pow(x,2) for x in subtract)/prediction.size),0.5)
    print ("loss = ", loss)
    return loss