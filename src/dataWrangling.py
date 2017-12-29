# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 13:32:16 2017

@author: Hubert
"""

import pandas as pd
import numpy as np

import datetime

def addHolidays(data, holidayCSV):
    data = data.assign(holiday = 0)
    counterNational = 0
    counterRegional = 0
    counterLocal = 0
    
    
    for i in range(0, 349):
        if(holidayCSV['locale'][i] == 'National'):
            mask = (data.year == holidayCSV['year'][i]) & (data.month == holidayCSV['month'][i]) & (data.day == holidayCSV['day'][i])
            if(holidayCSV.year[i] == 2017):
                '''print('Year:', holidayCSV.year[i])
                print('Month:', holidayCSV.month[i])
                print('Day:', holidayCSV.day[i])
                print(data[mask].count())'''
            counterNational = counterNational + 1
        elif(holidayCSV['locale'][i] == 'Regional'):
            mask =  (data.year == holidayCSV['year'][i]) & (data.month == holidayCSV['month'][i]) & (data.day == holidayCSV['day'][i]) & (data.state == holidayCSV['locale_name'][i])
            counterRegional = counterRegional + 1
        else:
            mask = (data.year == holidayCSV['year'][i]) & (data.month == holidayCSV['month'][i]) & (data.day == holidayCSV['day'][i]) & (data.city == holidayCSV['locale_name'][i])
            counterLocal = counterLocal + 1
            
        data.loc[mask, 'holiday'] = 1
    
    print("National:", counterNational)
    print("Regional:", counterRegional)
    print("Local:", counterLocal)
    
    return data

def pickItems(itemsDF):
    family_u = itemsDF.family.unique()
    sample = pd.DataFrame()    
    
    for i in range(0,family_u.size):
        sample = sample.append(itemsDF[itemsDF['family'] == family_u[i]].head(10))
        
    return sample

def movingAverages(oldData, itemsDF):
    
    data = oldData.copy(deep=True)
    
    #creates a unique list of stores and items from the dataset
    stores_u = data.store_nbr.unique()
    item_u = itemsDF.item_nbr.unique()

    data = data.set_index(['store_nbr', 'item_nbr'], drop = False)
    tmpa = pd.DataFrame()
    for i in stores_u:
        print("Store number", i)
        for item in item_u:
            #if((i,item) in  data.index):
                #print("i = <>, item = <>", (i, item))    
                tmp = data.loc[[(i,item)]]
                #for j in [112,56,28,14,7,3,1]:
                for j in [28,14,7,3,1]:
                    tmp['ma' + str(j)] = tmp.unit_sales.rolling(j).mean() 
                    tmp['ma' + str(j)] = tmp['ma' + str(j)].shift(1)
                    tmp['prev'+ str(j)] = tmp.unit_sales.shift(j)
                    #tmp['ma' + str(j)][1:len(tmp)] = tmp['ma' + str(j)][0:len(tmp)-1]
                tmpa = tmpa.append(tmp)
                tmp.drop(tmp.index, inplace=True)            



    data = pd.merge(data, tmpa, on=['store_nbr', 'item_nbr', 'date'])    
        
    return data
