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
dataTable = pd.read_sql_query(sqlString, conn)
states = dataTable.to_records()


#Inputs: Hardcoded for now
olfStateCd = 'PA'
typeOfCurve = "D"
lengthOfPeriodInMonths = 1
typeOfPeriod = "Accident"                           #"Policy", "Accident", or "Calendar"
policyTermInMonths = 12
typeOfOlf = 1
startDate = datetime.date(year=1998, month = 1, day = 1)   #This will be the minimum date of the interpolated level indices
endDate = datetime.date(year=2030, month =12, day =1)         #This will be the maximum date of the interpolated level indices. Should be far in the future.


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
dataTable = pd.read_sql_query(sqlString, conn, params = params)
dataTable['EffectiveDate'] = pd.to_datetime(dataTable['EffectiveDate']).dt.date


####################################################################################################################
########Interpolation Section          #############################################################################
####################################################################################################################

#First we'll build a column of factors based on the percent changes. Then cumulatively multiply them to build the LevelIndex.
dataTable['Factor'] = dataTable['PercentChange'].apply(MathMethods.factorBuilder)
dataTable['LevelIndex'] = np.cumprod(dataTable['Factor'])

#This part is brute force. We'll need to calculate the average date in between each date.
#To do this, we'll create a second column and shift the first dates up. This will naturally leave the last entry Null in the second date column. 
#We'll arbitrarily set this last entry to be 2 days after the latest entry. Note that timedelta doens't have a month offset.
firstDates = pd.to_datetime(dataTable['EffectiveDate']).dt.date
secondDates = pd.to_datetime(firstDates).shift(-1).dt.date
secondDates[len(secondDates) - 1] = max(secondDates) + datetime.timedelta(days = 2)

#Numpy.vectorize takes in a method and vectorizes it. We'll use it to finally create our average date column in the main datatable.
vfunc = np.vectorize(DateMethods.getAverageAccidentDate)
dataTable['AverageAccidentDate'] = vfunc(firstDates, secondDates, typeOfPeriod, policyTermInMonths)

#Now, instantiate a table of dates from some very early date to a date far in the future. 
#We'll want this range to cover all dates we have tracked changes for and far in the future dates we'll want to trend to.
interpolationTable = pd.DataFrame(pd.date_range(start=startDate, end=endDate, freq=str(lengthOfPeriodInMonths) + 'MS').date).rename(columns={0: 'TimePeriod'})

#This average accident date is more complicated than the midpoint. The original from excel is rounding the day for this instance. Also takes into account whether we're using policy or accident periods.
interpolationTable['AverageAccidentDate'] = interpolationTable['TimePeriod'].apply(DateMethods.getAverageAccidentDateMonthly, args=(typeOfPeriod, lengthOfPeriodInMonths))
