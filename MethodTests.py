# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 09:36:29 2022

@author: btran
"""

import numpy as np
import pandas as pd
from MathUtils import MathMethods

value = -16.546549846516132465489478415564
precision = 1

valueString= str(abs(np.float64(value)))
sign = ('-', '')[value>=0]
index = valueString.find('.')   

#print(value back if it's a whole number for now.
if (index == -1):
    print(float(value))
elif (precision >=0):
    valueString = valueString + ''.zfill(precision) #padding with zeroes to the right in case precision requested is bigger than number of digits to the right of decimal
    #This algorithm only works for nonnegative precision.. need to work on negative precision (-1 means round to tens, -2 hundreds, etc)
    leftOfPrecision = valueString[0:index + precision + 1]  #Left of the precision is all digits to left of required digits inclusive of digit being rounded
    rightOfPrecision = valueString[index + precision + 1:]  #Everything to the right of the above
    #Round up if first digit of the Right side is 5 or greater. Truncate if otherwise.
    if (int(rightOfPrecision[0]) >= 5):
        roundedNumber = str(float(leftOfPrecision.replace('.','')) + 1)
        roundedNumber = str(roundedNumber[0:index] + "." + roundedNumber[index:index + precision])
        print(sign + roundedNumber)
    else:
        roundedNumber = str(leftOfPrecision.replace('.',''))
        roundedNumber = str(roundedNumber[0:index] + "." + roundedNumber[index:index + precision])
        print(sign + roundedNumber)
else:
    print(value)
    


xInput = 1.5
xSeries = [1, 2]
distanceSeries = abs(xInput - xSeries)
distanceSeries = pd.concat([xSeries, distanceSeries], axis = 1)
minIndex = distanceSeries['distance'].idxmin()    

MathMethods.correctRound(2.85,1)

value = 2.85
precision = 1
sign = math.copysign(1, value) #need to use copysign since python doesn't support sign
temp = abs(value)*(10**precision)
temp = temp + 0.5
temp = math.trunc(temp)
temp = temp/(10**precision)
temp = temp * sign

xInput = 1.5
xSeries = [1,2]
ySeries = [2.3,4.2]
curveType = 'Discrete'
if (curveType == 'Continuous'):
    A = np.vstack([xSeries, np.ones(len(xSeries))]).T
    alpha = np.linalg.lstsq(A, ySeries, rcond=None)[0]
    yPrediction = alpha[0]*xInput + alpha[1]
    print(yPrediction)
elif (curveType == 'Discrete'):            
    print(MathMethods.findMinIndex(xInput, xSeries))

distanceSeries = pd.Series(abs(np.array(len(xSeries)*[xInput]) - np.array(xSeries))).rename('distance')
distanceSeries = pd.concat([pd.Series(xSeries), distanceSeries], axis = 1)
minIndex = distanceSeries['distance'].idxmin()
