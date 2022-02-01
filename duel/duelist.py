#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 14:20:28 2022

@author: Christopher Corbell
"""

from prob.pfunc import PFunc
import random

class Duelist:
    def __init__(self, position:int, aimfunction:PFunc, name):
        self.position = position
        self.aimfunction = aimfunction
        self.name = name
        
    def __repr__(self):
        return f"{self.name} is at {self.position}"
    
    def currentChance(self, targetPosition):
        distance = abs(self.position - targetPosition)
        #print (f"DEBUG: currentChance for {self.name}, distance is {distance}")
        chance = self.aimfunction.evaluate(distance)
        #print (f"DEBUG: currentChance for {self.name}, aimfunction returned {chance}")
        return chance
    
    def step(self, increment:int):
        """
        Take a step (incrementing one's position toward opponent)

        Parameters
        ----------
        increment : int
            The size and direction of the step to be taken, 
            typically 1 for the player that started at 0 and
            -1 for the player that started at the maximum position value.

        Returns
        -------
        None.

        """
        self.position += increment
        
    def fire(self, targetPosition:int):
        """
        Given the oponent's position, attempt to fire using
        probability of aimfunction at current distance.
        
        If uniform random number is <= chance returned by aim function,
        it's a success and the function returns True.

        Parameters
        ----------
        targetPosition : int
            The position of the opponent. Distance is the absolute value
            between targetPosition and player's current position.

        Returns
        -------
        bool
            True if the fire attempt is a hit, False if it is a miss.

        """
        chance = self.currentChance(targetPosition)
        attempt = random.uniform(0, 1)
        #print (f"DEBUG: chance is {chance}, attempt is {attempt}")
        if attempt <= chance:
            return True
        return False

        
    