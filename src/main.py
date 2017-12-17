# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 13:23:02 2017

@author: Hubert
"""

import InputOutput as io
import dataWrangling as dW
import xgboostTraining as xgbt

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

#Creating Verification set
nTrainRows = holidayTrainDF.shape[0]
if(verify):
    train = holidayTrainDF[:int(nTrainRows*0.8)]
    verification = holidayTrainDF[int(nTrainRows*0.8):]
    
if(model == 0): #Do XGBoost
    print("Running XGBoost Model")
    XGBModel = xgbt.trainXGModel(train, verification)