# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 23:24:34 2017

@author: Hubert
"""

import xgboost as xgb

def trainXGModel(train, verify):
    target = train['unit_sales']
    train.drop(['unit_sales'], axis=1)   
    xgtrain = xgb.DMatrix(train.values, target)
    
    xgModel = xgb.train()    
    return xgModel