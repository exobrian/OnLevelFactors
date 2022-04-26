# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:52:41 2022
Helper functions to handle math
@author: btran
"""
import datetime
import pandas as pd
import numpy as np
import math
from dateutil.relativedelta import relativedelta

class DateMethods:
    def getDaysInBetween(date1, date2):
        """        
        Parameters
        ----------
        date1 : datetime
            First date parameter.
        date2 : datetime
            Second date parameter.

        Returns
            The return type is 'int'. This is the absolute number of days in between the two date parameters.
        TYPE
            'int'.

        """
        if (date1 is None or date2 is None):
            return None
        else:        
            return abs((date1-date2).days)  #this returns an integer which is always truncated.
        
    def getAverageAccidentDate(date1, date2, typeOfPeriod="Accident", policyTermInMonths=12):
        """        
        Parameters
        ----------
        date1 : datetime
            First date parameter.
        date2 : datetime
            Second date parameter
        typeOfPeriod : int
            Type of period being tracked. i.e. Accident Period, Policy Period, Calendar Period.
        policyTermInMonths : TYPE
            How many months in period.

        Returns
            'datetime' that is the midpoint of the two date parameters
        TYPE
            'datetime'.

        """
        if (date1 is None or date2 is None):
            return None
        halfOfDaysBetween = MathMethods.correctRound(DateMethods.getDaysInBetween(date1, date2)/2, 0)
        midDate = min(date1, date2) + datetime.timedelta(days = halfOfDaysBetween)
        return midDate
    
    def getLatestDate(date1, dateSeries, returnIndex = 0):
        """      
        Parameters
        ----------
        date1 : TYPE
            DESCRIPTION.
        dateSeries : TYPE
            DESCRIPTION.
        returnIndex : TYPE, optional
            DESCRIPTION. The default is 0.
            Set to 1 to return ith entry in series. Set to 0 if only requiring index.
        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        dateDistanceSeries = pd.to_timedelta(abs(dateSeries - date1), unit='day').dt.days.rename('DateDistance')
        dateDistanceSeries = pd.concat([dateSeries, dateDistanceSeries], axis = 1)
        minDateIndex = dateDistanceSeries['DateDistance'].idxmin()
        
        if (returnIndex == 1):
            return minDateIndex
        else:
            return dateSeries[minDateIndex]
    
    def getAverageAccidentDateMonthly(date1, typeOfPeriod='Accident', lengthOfPeriodInMonths=1):
        typeOfPeriodOffset = (0,12)[typeOfPeriod=='Policy']
        year = date1.year    
        month = date1.month
        day = ((lengthOfPeriodInMonths + typeOfPeriodOffset) % 2)*14 + 1    #this just rounds the midpoint to the 15th day of the month for odd period lengths. Sets to 1st day for even period lengths.
        monthOffset = math.floor((lengthOfPeriodInMonths + typeOfPeriodOffset)/2)
        return datetime.date(year=year, month=month, day=day) + relativedelta(months=monthOffset)
    
class MathMethods:       
    def correctRound(value, precision = 0):
        """       
        Parameters
        ----------
        value : numerical
            This is the number to be round.
        precision : TYPE, optional
            DESCRIPTION. The default is 0.
            Precision is the desired decimal place to be rounded to.
            0 indicates nearest integer.
            1 indicates tenths place.
            2 indicates hundredths place.
            etc.

        Returns float
        -------
        TYPE
            Float rounded to user requested precision

        """
        sign = math.copysign(1, value) #need to use copysign since python doesn't support sign
        temp = abs(value)*(10**precision)
        temp = temp + 0.5
        temp = math.trunc(temp)
        temp = temp/(10**precision)
        temp = temp * sign
        return temp            
        
    def interpolate(xInput, xSeries, ySeries, curveType = 'Discrete'):
        if (curveType == 'Continuous'):
            A = np.vstack([xSeries, np.ones(len(xSeries))]).T
            alpha = np.linalg.lstsq(A, ySeries, rcond=None)[0]
            yPrediction = alpha[0]*xInput + alpha[1]
            return yPrediction
        elif (curveType == 'Discrete'):            
            minIndex = MathMethods.findMinIndex(xInput, xSeries)
            return ySeries[minIndex]
    
    def findMinIndex(xInput, xSeries):
        distanceSeries = pd.Series(abs(np.array(len(xSeries)*[xInput]) - np.array(xSeries))).rename('distance')
        distanceSeries = pd.concat([pd.Series(xSeries), distanceSeries], axis = 1)
        minIndex = distanceSeries['distance'].idxmin()
        return minIndex
       
    
class ExcelMethods:
    def IndexMatchColumn(dataSeries, rowIndex):
        return dataSeries[rowIndex]