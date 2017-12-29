# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 13:23:02 2017

@author: Hubert
"""

import InputOutput as io
import dataWrangling as dW
import xgboostTraining as xgbt

import numpy as np
import pandas as pd

import datetime

from sklearn.model_selection import train_test_split


#Settings used to save time if you need to
mode = 2 #used to determine whih dataset we're reading from
read = 0 #change to 1 if you want to re-read dataframes, otherwise, set this to 0
dataWrangle = 0 #change to 1 if you want to rewrangle data
verify = 0 #change to 1 if you want to remake the verification sets
model = 0


if(read):
    currentTime = datetime.datetime.now().isoformat()
    print("Reading time begin:", currentTime)
    
    print("Reading Training Database, mode {} ...".format(mode))
    trainDF = io.readTrainData(mode)
    
    print("Reading Test Database...")
    testDF = io.readTestData()
    
    print("Reading Holiday Database ...")
    holidayDF = io.readHoliday()
    
    print("Reading item list....")
    itemDF = io.readItemNbr()
    
    
    print("Read complete... ")
    finishTime = datetime.datetime.now().isoformat()
    print("Reading time ends:", finishTime)
    
else:
    print("Skipping Read...")

if(dataWrangle):
    newItemDF = dW.pickItems(itemDF)
    
    currentTime = datetime.datetime.now().isoformat()
    print("Moving Averages time begin:", currentTime)
    
    print("Implementing moving averages...")
    #trainDF = dW.movingAverages(trainDF)
    trainDF = dW.movingAverages(trainDF, newItemDF)
    
    finishTime = datetime.datetime.now().isoformat()
    print("Moving Averages time ends:", finishTime)

    newTrainDF = trainDF.copy(deep = True)
    newTrainDF = newTrainDF[newTrainDF.columns.drop(list(newTrainDF.filter(regex='_y')))]
    newTrainDF.columns = newTrainDF.columns.str.replace('_x','')
    
    currentTime = datetime.datetime.now().isoformat()
    print("Holiday training time begin:", currentTime)
    
    print("Adding holidays...")
    holidayTestDF = dW.addHolidays(testDF, holidayDF)
    holidayTrainDF = dW.addHolidays(newTrainDF, holidayDF)
    
    currentTime = datetime.datetime.now().isoformat()
    print("Holiday training time ends:", currentTime)
    
    
    currentTime = datetime.datetime.now().isoformat()
    print("Dummies time begin:", currentTime)
    
    print("Adding dummy variables...")
    dummyTrain = pd.get_dummies(holidayTrainDF)
    dummyTest = pd.get_dummies(holidayTestDF)
    
    currentTime = datetime.datetime.now().isoformat()
    print("Dummies time ends:", currentTime)
    
    nTrainRows = dummyTrain.shape[0]
    

#Creating Verification set
if(verify):
    currentTime = datetime.datetime.now().isoformat()
    print("Verification time begin:", currentTime)
    
    print("Set up verification tables...")
    train = dummyTrain[:int(nTrainRows*0.8)]
    verification = dummyTrain[int(nTrainRows*0.8):]
    
  #  xgTrain = train.drop(columns = ['date'])
    #xgVerify = verification.drop(columns = ['date'])
    
    train.to_csv("../../data/Processed/3012-1219-trainProcessed.csv")
    verification.to_csv("../../data/Processed/3012-1219-VerifyProcessed.csv")
    
    currentTime = datetime.datetime.now().isoformat()
    print("Verification time ends:", currentTime)
        
    
if(model == 0): #Do XGBoost
    print("Dropping date and item number...")

    #xgTrain = pd.read_csv("../../data/Processed/xgTrainProcessed.csv")
    xgTrain = pd.read_csv("../../data/Processed/3012-1219-trainProcessed.csv")
    
    print("training XGBoost Model")
    XGBModel = xgbt.trainXGModel(xgTrain)
    
    xgVerify = pd.read_csv("../../data/Processed/3012-1219-VerifyProcessed.csv")
    xgVerifyScores = xgVerify['unit_sales']
    xgVerify = xgVerify.drop(['unit_sales'], axis=1)
    
    scores = xgVerifyScores.values #converts scores to values 
    
    del xgTrain    
    
    predictions = XGBModel.predict(xgVerify)
    
    predictions[predictions < 0] = 0
    scores[scores < 0] = 0
    
    np.savetxt("../../predictions2.csv", predictions, delimiter = ",")
    
    loss = xgbt.loss(predictions, scores)
    
    