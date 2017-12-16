# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 13:23:02 2017

@author: Hubert
"""

import InputOutput as io
import dataWrangling as dW

import datetime as dt

#Settings used to save time if you need to
mode = 2 #used to determine whih dataset we're reading from
read = 0 #change to 1 if you want to re-read dataframes, otherwise, set this to 0
dataWrangle = 0 #change to 1 if you want to rewrangle data


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

print("Adding holidays...")
newTestDF = dW.addHolidays(testDF, holidayDF)
#newTrainDF = dW.addHolidays(trainDF, holidayDF)