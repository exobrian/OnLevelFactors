# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:52:41 2022
Helper functions to handle math
@author: btran
"""
import datetime
import pandas as pd
import math

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
        
    def getAverageAccidentDate(date1, date2, typeOfPeriod, policyTermInMonths):
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
        if (math.isnan(date1) or math.isnan(date2)):
            return math.nan
        halfOfDaysBetween = MathMethods.correctRound(DateMethods.getDaysInBetween(date1, date2)/2, 0)
        midDate = min(date1, date2) + datetime.timedelta(days = halfOfDaysBetween)
        return midDate
    
    def getLatestDate(date1, dateSeries):        
        dateDistanceSeries = pd.to_timedelta(abs(dateSeries - date1), unit='day').dt.days.rename('DateDistance')
        dateDistanceSeries = pd.concat([dateSeries, dateDistanceSeries], axis = 1)
        minDateIndex = dateDistanceSeries['DateDistance'].idxmin()
        return dateSeries[minDateIndex]
        
    
class MathMethods:
    def correctRound(value, precision = 0):
        valueString= str(abs(value))    
        sign = (-1, 1)[value>=0]
        index = valueString.find('.')   
        
        #return value back if it's a whole number for now.
        if (index == -1):
            return float(value)
        elif (precision >=0):
            valueString = valueString + ''.zfill(precision) #padding with zeroes to the right in case precision requested is bigger than number of digits to the right of decimal
            #This algorithm only works for nonnegative precision.. need to work on negative precision (-1 means round to tens, -2 hundreds, etc)
            leftOfPrecision = valueString[0:index + precision + 1]  #Left of the precision is all digits to left of required digits inclusive of digit being rounded
            rightOfPrecision = valueString[index + precision + 1:]  #Everything to the right of the above
            #Round up if first digit of the Right side is 5 or greater. Truncate if otherwise.
            if (int(rightOfPrecision[0]) >= 5):
                roundedNumber = str(float(leftOfPrecision.replace('.','')) + 1)
                roundedNumber = float(str(roundedNumber[0:index] + "." + roundedNumber[index:index + precision]))
                return roundedNumber * sign
            else:
                roundedNumber = str(float(leftOfPrecision.replace('.','')))
                roundedNumber = float(str(roundedNumber[0:index] + "." + roundedNumber[index:index + precision]))
                return roundedNumber * sign
        else:
            return value
    
    def factorBuilder(i):
        return (1+i)