#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 23:51:10 2022

@author: Christopher Corbell
"""
import random

class Dice:
    D6 = [n for n in range(1, 7)]
    D20 = [n for n in range(1, 21)]
    
    def d6():
        return random.choice(Dice.D6)
    
    def d20():
        return random.choice(Dice.D20)
    
    def nd6(n:int):
        rolls = []
        for i in range(0, n):
            rolls.append(Dice.d6())
        return rolls
    
    def nd6sum(n:int):
        return sum(Dice.nd6(n))
    
       
    def nd20(n:int):
        rolls = []
        for i in range(0, n):
            rolls.append(Dice.d20())
        return rolls
    
    def nd20sum(n:int):
        return sum(Dice.nd20(n))
    
     