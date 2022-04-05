# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:52:41 2022
Helper functions to handle math
@author: btran
"""
import datetime
import pandas as pd
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
    
    def getLatestDate(date1, dateSeries):        
        dateDistanceSeries = pd.to_timedelta(abs(dateSeries - date1), unit='day').dt.days.rename('DateDistance')
        dateDistanceSeries = pd.concat([dateSeries, dateDistanceSeries], axis = 1)
        minDateIndex = dateDistanceSeries['DateDistance'].idxmin()
        return dateSeries[minDateIndex]    
    
    def getAverageAccidentDateMonthly(date1, typeOfPeriod='Accident', lengthOfPeriodInMonths=1):
        typeOfPeriodOffset = (0,12)[typeOfPeriod=='Policy']
        year = date1.year    
        month = date1.month
        day = ((lengthOfPeriodInMonths + typeOfPeriodOffset) % 2)*14 + 1
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
            Note: Precision less than 0 currently not supported

        Returns float
        -------
        TYPE
            This method converts input into a string before recasting as float.

        """
        valueString= str(abs(value))    
        sign = ('-', '')[value>=0]
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
                roundedNumber = str(roundedNumber[0:index] + "." + roundedNumber[index:index + precision])
                return float(sign + roundedNumber)
            else:
                roundedNumber = str(leftOfPrecision.replace('.',''))
                roundedNumber = str(roundedNumber[0:index] + "." + roundedNumber[index:index + precision])
                return float(sign + roundedNumber)
        else:
            return value
    
    def factorBuilder(i):
        return (1+i)