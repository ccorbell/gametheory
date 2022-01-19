#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 23:08:28 2022

@author: mathaes
"""
import random

class RandomWalk:
    
    def __init__(self, dimension = 1):
        self.dimension = dimension
        self.origin = [0] * self.dimension
        self.position = self.origin.copy()
        # generate moves by dimension index;
        # negative moves are these -self.dimension
        posMoves = [n for n in range(0, self.dimension)]
        negMoves = [item - dimension for item in posMoves]
        self.moves = posMoves + negMoves
        self.moveCount = 0
        self.maxMoves = 10000
        self.verbose = False
        
    def move(self):
        moveValue = random.choice(self.moves)
        if moveValue < 0:
            index = moveValue + self.dimension
            self.position[index] -= 1
        else:
            self.position[moveValue] += 1
        self.moveCount += 1
        if self.verbose:
            print (self.position)
        
    def run(self):
        if self.verbose:
            print(f"Running randomWalk in {self.dimension} dimensions, maxMoves {self.maxMoves}...")
            
        self.moveCount = 0
        self.position = self.origin.copy()
        self.move()
        while not self.position == self.origin:
            self.move()
            if self.moveCount >= self.maxMoves:
                break
        
        success = self.position == self.origin
        if self.verbose:
            if success:
                print(f"Random walk SUCCESS - returned to origin in {self.moveCount} steps.")
            else:
                print(f"Random walk FAILURE: did not return to origin after {self.moveCount} steps.")
        
        return (success, self.moveCount)