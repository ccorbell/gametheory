#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 23:06:16 2022

@author: mathaes
"""

class PFunc:
    """
    A PFunc is a representation of a probability function.
    
    A PFunc may be discrete or continuous but is expected to
    be able to produce a value in the interval [0,1] for any input,
    though subclasses may throw exceptions for unsupported inputs.
    """
    
    def __init__(self):
        pass
    
    def evaluate(self, inputValue):
        return 0.0
    
class LinearRangePFunc:
    
    def __init__(self, minVal, maxVal, minProb=100.0, maxProb=0.0):
        self.minVal = minVal
        self.maxVal = maxVal
        self.minProb = minProb
        self.maxProb = maxProb
        
    def evaluate(self, inputValue):
        if inputValue <= self.minVal:
            return self.minProb
        elif inputValue >= self.maxVal:
            return self.maxProb
        else:
            offset = inputValue - self.minVal
            valueRange = self.maxVal - self.minVal
            probRange = self.maxProb - self.minProb
            return (offset / valueRange) * probRange + self.minProb
        
    