# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:52:41 2022
Helper functions to handle math
@author: btran
"""
import datetime

class DateMethods:
    def getDaysInBetween(date1, date2):
        if (date1 is None or date2 is None):
            return None
        else:        
            return abs((date1-date2).days)  #this returns an integer which is always truncated.
        
    def getAverageAccidentDate(date1, date2, typeOfPeriod, policyTermInMonths):
        #if typeOfPeriod == 'Policy':
        halfOfDaysBetween = MathMethods.correctRound(DateMethods.getDaysInBetween(date1, date2)/2, 0)
        midDate = min(date1, date2) + datetime.timedelta(days = halfOfDaysBetween)
        return midDate
    
class MathMethods:
    def correctRound(value, precision = 0):
        valueString= str(value)
        index = valueString.find('.')   
        
        if (index == -1 and precision >= 0):
            return float(value)
        else:        
            leftOfPrecision = valueString[0:index + precision + 1]  #Left of the precision is all digits to left of required digits inclusive of digit being rounded
            rightOfPrecision = valueString[index + precision + 1:]  #Everything to the right of the above
            if (int(rightOfPrecision[0]) >= 5):
                roundedNumber = str(float(leftOfPrecision.replace('.','')) + 1)
                roundedNumber = float(str(roundedNumber[0:index] + "." + roundedNumber[index:index + precision]))
                return roundedNumber
            else:
                roundedNumber = str(float(leftOfPrecision.replace('.','')))
                roundedNumber = float(str(roundedNumber[0:index] + "." + roundedNumber[index:index + precision]))
                return roundedNumber
        return None