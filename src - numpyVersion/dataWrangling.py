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

def rollingMean(values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma
    
def movingAverages(data, itemsDF):
    
    saleData = data[['id', 'item_nbr', 'date', 'store_nbr', 'unit_sales']]
    
    stores_u = saleData.store_nbr.unique()
    #item_u = itemsDF.item_nbr.unique()
    item_u = saleData.item_nbr.unique()
    
    
    
    
    #data = oldData.copy(deep=True)
    
    #creates a unique list of stores and items from the dataset
    #stores_u = data.store_nbr.unique()
    #item_u = itemsDF.item_nbr.unique()
    derp = saleData.groupby('store_nbr')['unit_sales'].rolling(3)
    saleData = saleData.set_index(['store_nbr', 'item_nbr'], drop = False)
    #saleData = saleData.groupby('store_nbr')
    #saleData = saleData.sort_values(by = ['store_nbr', 'item_nbr'])

    tmpa = pd.DataFrame()
    for i in stores_u:
    #for i in saleData.groupby('store_nbr'):
        print("Store number", i)
        currentTime = datetime.datetime.now().isoformat()
        print("Store begin:", currentTime)
        for item in item_u:
            #if((i,item) in  data.index):
                #print("i = <>, item = <>", (i, item))    
                #currentTime = datetime.datetime.now().isoformat()
                #print("Copy begin:", currentTime)  
                tmp = saleData.loc[[(i,item)],:].copy()
                #for j in [112,56,28,14,7,3,1]:
                
                #currentTime = datetime.datetime.now().isoformat()
                
                tmpArray = tmp.unit_sales.values
                tmpArray = tmpArray.astype(float)
                
                #print("Section 1 time begin:", currentTime)                
                prev1 = shiftDown(tmpArray, 1)
                prev3 = shiftDown(prev1, 2)
                prev7 = shiftDown(prev3, 4)
                prev14 = shiftDown(prev7, 7)
                prev28 = shiftDown(prev14, 14)
                
                #for j in [28,14,7,3,1]:
                #    tmp['prev'+ str(j)] = tmp.unit_sales.shift(j)
                #currentTime = datetime.datetime.now().isoformat()
                #print("Section 2 time begin:", currentTime)
            
                
                ma1 = rolling_sum(tmpArray, 1)
                ma3 = rolling_sum(tmpArray, 3)
                ma7 = rolling_sum(tmpArray, 7)
                ma14 = rolling_sum(tmpArray, 14)
                ma28 = rolling_sum(tmpArray, 28)
                ma60 = rolling_sum(tmpArray, 60)
                ma90 = rolling_sum(tmpArray, 90)
                
                tmp['ma1'] = ma1
                tmp['ma3'] = ma3
                tmp['ma7'] = ma7
                tmp['ma14'] = ma14
                tmp['ma28'] = ma28
                tmp['ma60'] = ma60
                tmp['ma90'] = ma90
                
                
                tmp['prev1'] = prev1
                tmp['prev3'] = prev3
                tmp['prev7'] = prev7
                tmp['prev14'] = prev14
                tmp['prev28'] = prev28
                '''
                for j in [28,14,7,3,1]:
                    #temp1 = tmp.loc[:,'unit_sales'].rolling(j).mean()
                    temp1 = rollingMean(tmp.loc[:,'unit_sales'].values, j)
                    tmp.loc[:,'ma' + str(j)] = temp1
                    tmp.loc[:,'ma' + str(j)] = tmp.loc[:,'ma' + str(j)].shift(1)
                    tmp.loc[:,'prev'+ str(j)] = tmp.unit_sales.shift(j)
                    #tmp['ma' + str(j)][1:len(tmp)] = tmp['ma' + str(j)][0:len(tmp)-1]
                '''    
                currentTime = datetime.datetime.now().isoformat()
                #print("Section 3 time begin:", currentTime)
                tmpa = tmpa.append(tmp)
                currentTime = datetime.datetime.now().isoformat()
                #print("Section 4 time begin:", currentTime)
                tmp.drop(tmp.index, inplace=True)            



    data = data.merge(tmpa, on=['id', 'store_nbr', 'item_nbr', 'date'])    
        
    return data

def rolling_sum(a, n) :
    ret = np.cumsum(a, dtype=float)/n
    ret[n:] = ret[n:] - ret[:-n]
    if a.size > n:
        for i in range (n-1) :
            ret[i] = np.nan
    ret = np.insert(ret, 0, np.nan)
    return ret[:-1]

def shiftDown(data, n):
     if data.size > n:
        for i in range(n):
            data = np.insert(data, 0, np.nan)
        return data[:-n]
     else:
        return data