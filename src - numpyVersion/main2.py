# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 18:14:32 2018

@author: Hubert
"""

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

from xgboost import plot_importance
from matplotlib import pyplot

from sklearn.model_selection import train_test_split


#Settings used to save time if you need to
mode = 3 #used to determine whih dataset we're reading from
read = 1 #change to 1 if you want to re-read dataframes, otherwise, set this to 0
dataWrangle = 1 #change to 1 if you want to rewrangle data
verify = 1 #change to 1 if you want to remake the verification sets
model = 0


if(read):
    currentTime = datetime.datetime.now().isoformat()
    print("Reading time begin:", currentTime)
    
    print("Reading Training Database, mode {} ...".format(mode))
    trainArray = io.readTrainData(mode)
    
    print("Reading Test Database...")
    testArray = io.readTestData()
    
    print("Reading Holiday Database ...")
    holidayArray = io.readHoliday()
    
    print("Reading item list....")
    itemArray = io.readItemNbr()
    
    
    print("Read complete... ")
    finishTime = datetime.datetime.now().isoformat()
    print("Reading time ends:", finishTime)