# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 23:24:34 2017

@author: Hubert
"""

import xgboost as xgb
import sklearn
import numpy as np
import pandas as pd

from tqdm import tqdm

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

def predictXGBoost(xgModel, test, items, cols):
    
    df_2017 = test.set_index(
    ["store_nbr", "item_nbr", "date"])[["unit_sales"]].unstack(
        level=-1).fillna(0)
    df_2017.columns = df_2017.columns.get_level_values(1)
    df_2017['item_nbr'] = df_2017.index.get_level_values('item_nbr')
    df_2017['store_nbr'] = df_2017.index.get_level_values('store_nbr')

    #test = pd.get_dummies(test)
    '''
    test = pd.get_dummies(test, prefix = ['onpromotion', 'family', 'perishable', 'city', 'state', 'type'], 
                               columns =['onpromotion', 'family', 'perishable', 'city', 'state', 'type'])
    '''
    
    items = items.reindex(df_2017.index.get_level_values(1))
    
    
    base = datetime.date(day = 16, month = 8, year = 2017)
    date_list = [base + datetime.timedelta(days=x) for x in range(0, 16)]
    
    test['date'] = pd.to_datetime(test['date'])
    #test = convertDate(test)
    
    for date in tqdm(date_list):
        X = prepare_dataset(df_2017, date)
        dateResults = test[test['date'] == date]
        newData = pd.merge(dateResults, X, on = ['item_nbr', 'store_nbr'], how = 'outer')
        #dateFormat = newData['date'][1]
        newData = newData.drop(['date', 'unit_sales'], axis = 1)
        newData = pd.get_dummies(newData)
        newData.columns = newData.columns.str.strip()
        newData = newData[cols]
        predictions = xgModel.predict(newData)
        
        dateResults['unit_sales'] = pd.Series(predictions)
        test = pd.merge(test, dateResults, left_on = 'id', right_on = 'id', how = 'outer')
        test.unit_sales_x = test.unit_sales_x.fillna(0)
        test.unit_sales_y = test.unit_sales_y.fillna(0)
        test.unit_sales_x = test.unit_sales_x + test.unit_sales_y
        test = drop_y(test)
        test = rename_x(test)
        
        df_2017 = test.set_index(
        ["store_nbr", "item_nbr", "date"])[["unit_sales"]].unstack(
            level=-1).fillna(0)
        df_2017.columns = df_2017.columns.get_level_values(1)
        df_2017['item_nbr'] = df_2017.index.get_level_values('item_nbr')
        df_2017['store_nbr'] = df_2017.index.get_level_values('store_nbr')

    
    
    return test
    
#    for date in tqdm(date_list)
#        test[]
    
def get_timespan(df, dt, minus, periods):
    return df[pd.date_range(dt - datetime.timedelta(days=minus), periods=periods).applymap(str)]

def prepare_dataset(df, t2017, is_train=True):
    X = get_timespan(df, t2017, 14, 14)
    X.columns = ['unit_sales_lag14', 'unit_sales_lag13',
                 'unit_sales_lag12', 'unit_sales_lag11',
                 'unit_sales_lag10', 'unit_sales_lag9',
                 'unit_sales_lag8', 'unit_sales_lag7',
                 'unit_sales_lag6', 'unit_sales_lag5',
                 'unit_sales_lag4', 'unit_sales_lag3',
                 'unit_sales_lag2', 'unit_sales_lag1',
                 ]
    for i in range(1,15):
        X['unit_sales_MA' + str(i)] = get_timespan(df, t2017, i, i).mean(axis=1).values
    
    X.reset_index(level = ['store_nbr', 'item_nbr'], inplace = True)
    
    return X

def drop_y(df):
    # list comprehension of the cols that end with '_y'
    to_drop = [x for x in df if x.endswith('_y')]
    df.drop(to_drop, axis=1, inplace=True)
    
    return df
    
def rename_x(df):
    for col in df:
        if col.endswith('_x'):
            df.rename(columns={col:col.rstrip('_x')}, inplace=True)
            
    return df