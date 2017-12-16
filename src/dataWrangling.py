# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 13:32:16 2017

@author: Hubert
"""

import pandas as pd
import numpy as np


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
        