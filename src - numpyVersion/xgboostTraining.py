# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 23:24:34 2017

@author: Hubert
"""

import xgboost as xgb
import sklearn
import numpy as np
import pandas as pd

import tqdm

import datetime

from sklearn import preprocessing

import math

def trainXGModel(train):
    target = train['unit_sales']
    train['unit_sales'] = train['unit_sales'].astype('category')
    
    train = train.drop(['unit_sales'], axis=1)   
    
    currentTime = datetime.datetime.now().isoformat()
    print("Train time begin:", currentTime)
    xgModel = xgb.XGBRegressor(learning_rate = 0.3, n_estimators=30).fit(train, target)
    finishTime = datetime.datetime.now().isoformat()
    print("Train time finish:", finishTime)
    return xgModel

def loss(prediction, values):
    subtract = np.subtract([np.log1p(x) for x in prediction], [np.log1p(x) for x in values])
    print("Subtract = ", subtract)
    loss = pow((np.sum(pow(x,2) for x in subtract)/prediction.size),0.5)
    print ("loss = ", loss)
    return loss

def predictXGBoost(xgModel, test, items):
    results = pd.DataFrame
    
    df_2017 = test.set_index(
    ["store_nbr", "item_nbr", "date"])[["unit_sales"]].unstack(
        level=-1).fillna(0)
    df_2017.columns = df_2017.columns.get_level_values(1)

    items = items.reindex(df_2017.index.get_level_values(1))
    
    
    base = datetime.date(day = 16, month = 8, year = 2017)
    date_list = [base + datetime.timedelta(days=x) for x in range(0, 16)]
    
    test['dateIndex'] = test['date']
    
    test['date'] = pd.to_datetime(test['date'])
    #test = convertDate(test)
    
    for date in date_list:
        print(date)
    
    
    return test
    
#    for date in tqdm(date_list)
#        test[]
    
def get_timespan(df, dt, minus, periods):
    return df[pd.date_range(dt - datetime.timedelta(days=minus), periods=periods)]

def prepare_dataset(df, t2017, is_train=True):
    X = pd.DataFrame()
    
    for i in range(14):
        X['unit_sales_lag' + str(i)] = get_timespan(df, t2017, i, i).values 
        X['unit_sales_lag' + str(i)] = get_timespan(df, t2017, i, i).mean(axis=1).values
    return X