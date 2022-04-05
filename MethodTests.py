# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 09:36:29 2022

@author: btran
"""

import numpy as np

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