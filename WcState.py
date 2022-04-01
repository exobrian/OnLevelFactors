# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 13:52:05 2022

@author: btran
"""

class UsState:
    #Constructor
    def __init__(self, stateCode, stateName, isMainState, isWcSt, isWcAo):
        self.stateCode = stateCode
        self.stateName = stateName
        self.isMainState = isMainState
        self.isWcSt = isWcSt
        self.isWcAo = isWcAo
        
    
#class stateOlfIndices(object):