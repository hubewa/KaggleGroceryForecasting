# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 13:23:02 2017

@author: Hubert
"""

import InputOutput as io
import dataWrangling as dW
import xgboostTraining as xgbt

import pandas as pd

from sklearn.model_selection import train_test_split


import datetime as dt

#Settings used to save time if you need to
mode = 2 #used to determine whih dataset we're reading from
read = 0 #change to 1 if you want to re-read dataframes, otherwise, set this to 0
dataWrangle = 0 #change to 1 if you want to rewrangle data
verify = 0 #change to 1 if you want to remake the verification sets
model = 0


if(read):
    print("Reading Training Database, mode {} ...".format(mode))
    trainDF = io.readTrainData(2)
    
    print("Reading Test Database...")
    testDF = io.readTestData()
    
    print("Reading Holiday Database ...")
    holidayDF = io.readHoliday()
    
    
    print("Read complete... ")
else:
    print("Skipping Read...")

if(dataWrangle):
    print("Adding holidays...")
    holidayTestDF = dW.addHolidays(testDF, holidayDF)
    holidayTrainDF = dW.addHolidays(trainDF, holidayDF)
    
    print("Adding dummy variables...")
    dummyTrain = pd.get_dummies(holidayTrainDF)
    dummyTest = pd.get_dummies(holidayTestDF)
    
    nTrainRows = dummyTrain.shape[0]
    

#Creating Verification set
if(verify):
    print("Set up verification tables...")
    train = dummyTrain[:int(nTrainRows*0.8)]
    verification = dummyTrain[int(nTrainRows*0.8):]
    
    xgTrain = train.drop(columns = ['date','item_nbr'])
    xgVerify = train.drop(columns = ['date','item_nbr'])
    
    xgTrain.to_csv("../../data/Processed/xgTrainProcessed.csv")
    xgVerify.to_csv("../../data/Processed/xgVerifyProcessed.csv")
        
    
if(model == 0): #Do XGBoost
    print("Dropping date and item number...")

    xgTrain = pd.read_csv("../../data/Processed/xgTrainProcessed.csv")

    
    print("training XGBoost Model")
    XGBModel = xgbt.trainXGModel(xgTrain)
    
    xgVerify = pd.read_csv("../../data/Processed/xgVerifyProcessed.csv")
    xgVerifyScores = xgVerify['unit_sales']
    xgVerify = xgVerify.drop(['unit_sales'], axis=1)
    
    scores = xgVerifyScores.values #converts scores to values 
    
    del xgTrain    
    
    predictions = XGBModel.predict(xgVerify)
    
    predictions[predictions < 0] = 0
    scores[scores < 0] = 0
    
    loss = xgbt.loss(predictions, scores)
    
    