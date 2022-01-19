#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 23:01:56 2022

@author: Christopher Corbell
"""

import random

class CoinToss:
    
    HT = ['H', 'T']
    
    def __init__(self):
        self.headsP = 0.5
        
    def toss(self):
        if 0.5 == self.headsP:
            return random.choice(CoinToss.HT)
        else:
            if random.uniform(0.0, 1.0) <= self.headsP:
                return 'H'
            else:
                return 'T'
        
    def run(self, trials):
        """
        Run a trial of some number of coin tosses

        Parameters
        ----------
        trials : int
            The number of coin tosses to run.

        Returns
        -------
        The number of heads from the trial.

        """
        headCount = 0
        for n in range(0, trials):
            if self.toss() == 'H':
                headCount += 1
        return headCount