# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 10:41:04 2022

@author: btran

User should pass in either a state or a group of states and an accident date to trend to.
Then, this code should calculate all the on level factors requested. Maybe assume monthly factors unless
arguments supplied to convert to a different period.

First part:
    Sql database should be set up.
    Each state owner should have an excel macro button to upload the indices or the changes from one effective date to the next.
    These will be by state, index type, policy year/accident year, interpolation type (discrete or continuous) etc.
    
Second part:
    This code should pull all these changes, calculate the interpolated levels for each state and olf type, then generate weighted and unweighted olfs for the trended date selected.
"""

import pyodbc 
import pandas as pd
import numpy as np
#from datetime import date
import datetime

from MathUtils import DateMethods, MathMethods


"""Alternative Driver: ODBC Driver 17 for SQL Server"""
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DC1BISQLDEV01;'
                      'Database=ActuarialSandbox;'
                      'Trusted_Connection=yes;')

sqlString = 'SELECT * FROM dimState'

#cursor = conn.cursor()
#cursor.execute('SELECT * FROM dimState')
"""print(type(cursor))
for i in cursor:
    print(i)
"""
dataTable = pd.read_sql_query(sqlString, conn)
#newState = UsState(dataTable.iloc[1])

states = dataTable.to_records()
print(states[0])


#Inputs: Hardcoded for now
olfStateCd = 'PA'
typeOfCurve = "D"
lengthOfPeriodInMonths = 1
typeOfPeriod = "Accident"                           #"Policy", "Accident", or "Calendar"
policyTermInMonths = 12
typeOfOlf = 1
startDate = (date(year=1998, month = 1, day = 1))   #This will be the minimum date of the interpolated level indices
endDate = date(year=2030, month =12, day =1)         #This will be the maximum date of the interpolated level indices


nextDate = pd.Timestamp(startDate) + pd.DateOffset(months=lengthOfPeriodInMonths)

#Fetching id for State
sqlString = 'Select top (1) id from dimState with (nolock) where StateCd = ?'
params = olfStateCd
cursor = conn.cursor()
cursor.execute(sqlString, params)
olfStateId = cursor.fetchone()[0]

#Getting table of indices
sqlString = 'Select Max(UploadDate) from OnlevelFactors where stateDimId = ?' 
params = str(olfStateId)
cursor.execute(sqlString, params)
maxUploadDate = cursor.fetchone()[0]

sqlString = """Select EffectiveDate, PercentChange From OnLevelFactors with (nolock)
        Where UploadDate = ?
        and OlfTypeDimId = ?
        and StateDimId = ?
        """
params = (maxUploadDate, typeOfOlf, olfStateId)            
dataTable = pd.read_sql_query(sqlString, conn, params = params)#, index_col = 'EffectiveDate')
dataTable['EffectiveDate'] = pd.to_datetime(dataTable['EffectiveDate']).dt.date


####################################################################################################################
########Interpolation Section          #############################################################################
####################################################################################################################
#testing date lookup. Not sure why, but lookup value needs to be a string even though index column is datetime.
#This line will look up the latest date up to what's requested
#dataTable.iloc[dataTable.index.get_loc(str(nextDate), method='ffill')]
dataTable.iloc[dataTable['EffectiveDate'].get_loc(str(nextDate), method='ffill')]
#dataTable.loc[dataTable['EffectiveDate']==startDate]

print(DateMethods.getAverageAccidentDate(startDate, endDate, 1, 12))

#First we'll build a column of factors based on the percent changes. Then cumulatively multiply them to build the LevelIndex.
dataTable['Factor'] = dataTable['PercentChange'].apply(MathMethods.factorBuilder)
dataTable['LevelIndex'] = np.cumprod(dataTable['Factor'])


startDate = (date(year=1998, month = 1, day = 1))
interpolationTable = pd.date_range(start=startDate, end=endDate, freq=str(lengthOfPeriodInMonths) + 'MS', name='TimePeriod').date
firstDates = pd.to_datetime(dataTable['EffectiveDate']).dt.date
secondDates = pd.to_datetime(dataTable['EffectiveDate'].shift(-1)).dt.date
max(secondDates) + datetime.timedelta(days = 2) #doesn't really matter what this date is. Need it to fill NaN space to match sizes between arrays.

vfunc = np.vectorize(DateMethods.getAverageAccidentDate)
vfunc(firstDates, secondDates, 1,12)

dataTable['AverageAccidentDate'] = DateMethods.getAverageAccidentDate(firstDates, secondDates, typeOfPeriod, policyTermInMonths)
