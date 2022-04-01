# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 09:36:29 2022

@author: btran
"""
value = 182.5
precision = 0

valueString= str(value)
index = valueString.find('.')   

if (index == -1 and precision >= 0):
    print(float(value))
else:        
    leftOfPrecision = valueString[0:index + precision + 1]  #Left of the precision is all digits to left of required digits inclusive of digit being rounded
    rightOfPrecision = valueString[index + precision + 1:]  #Everything to the right of the above
    
    if (int(rightOfPrecision[0]) >= 5):
        roundedNumber = str(float(leftOfPrecision.replace('.','')) + 1)
        roundedNumber = float(str(roundedNumber[0:index] + "." + roundedNumber[index:index + precision]))
        print(roundedNumber)
    else:
        roundedNumber = str(float(leftOfPrecision.replace('.','')))
        roundedNumber = float(str(roundedNumber[0:index] + "." + roundedNumber[index:index + precision]))
        print(roundedNumber)