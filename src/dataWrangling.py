# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 13:32:16 2017

@author: Hubert
"""

import pandas as pd
import numpy as np


def addHolidays(data, holidayCSV):
    data = data.assign(holiday = 0)
    
    
    for i in range(0, 349):
        if(holidayCSV.locale[i] == 'National'):
            data.loc[data.date == holidayCSV['date'][i], 'holiday'] = 1
        elif(holidayCSV.locale[i] == 'Regional'):
            data.loc[(data.date == holidayCSV['date'][i]) & (data.state == holidayCSV['locale_name'][i]), 'holiday'] = 1
        else:
            data.loc[(data.date == holidayCSV['date'][i]) & (data.city == holidayCSV['locale_name'][i]), 'holiday'] = 1
    
    
    return data
        