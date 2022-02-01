#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 14:12:37 2022

@author: mathaes
"""

from duel.duelist import Duelist
from prob.pfunc import PFunc, LinearRangePFunc

class Duel:
    """
    Duel is a turn-based game where two duelists take turns deciding to either
    take a step forward or aim and fire. Aim is implemented as a probabilistic 
    function of distance (subclass of prob.pbfunc.PBFunc). Each player can have 
    their own aim function. Distance is an integer difference between the
    two players' positions. A step always brings a player 1 unit closer
    to their opponent.
    
    
    
    """
    def __init__(self, 
                 distance=20,
                 player1func: PFunc = None,
                 player2func: PFunc = None):
        self.minPos = 0
        self.maxPos = distance

        if None == player1func:
            player1func = LinearRangePFunc(1, distance, 1.0, 0.0)
            
        if None == player2func:
            player2func = LinearRangePFunc(1, distance, 0.65, 0.2)
            
        self.players = [Duelist(0, player1func,  "Bozo"),
                        Duelist(distance, player2func, "Bubbles")]
        self.gameRound = 0
        self.gameOver = False
        self.winnerIndex = -1
        
    def resetGame(self):
        self.gameRound = 0
        self.players[0].position = 0
        self.players[1].position = self.maxPos
        self.gameOver = False
        
    def runAimChanceThesholdGame(self, player1Threshold = 0.6, player2Threshold = 0.5):
        self.resetGame()
        
        self.players[0].position = self.minPos
        self.players[1].position = self.maxPos
        
        print ("*** CLOWN PIE DUEL ***")
        print (f"{self.players[0].name} vs. {self.players[1].name} square off,")
        print (f"  pies in hand, at {self.maxPos - self.minPos} paces.\n")
        
        print ("The duel begins...")
        
        while not self.gameOver:
            
            playerIndex = self.gameRound % 2
            opponentIndex = (playerIndex +  1) % 2
            
            player = self.players[playerIndex]
            opponent = self.players[opponentIndex]
            
            # see if player is at their aim chance threshold
            chanceCheck = player.currentChance(opponent.position)
            threshold = player1Threshold
            if playerIndex == 1:
                threshold = player2Threshold
                
            #print (f"DEBUG: chanceCheck is {chanceCheck}, threoshold is {threshold}")
            timeToFire = chanceCheck >= threshold
            if timeToFire:
                
                print (f"\n{player.name} LAUNCHES A PIE!")
                print (f" ({player.name}'s odds of hitting are {player.currentChance(opponent.position)*100} %)")
                fireResult = player.fire(opponent.position)
                
                if True == fireResult:
                    print (f"{player.name} has hit their opponent.")
                    self.winnerIndex = playerIndex
                else:
                    print (f"{player.name} has missed their opponent.")
                    self.winnerIndex = opponentIndex
                self.gameOver = True
            else:
                stepIncrement = 1
                if playerIndex == 1:
                    stepIncrement = -1
                print(f"{player.name} takes a step forward.")
                player.step(stepIncrement)
                
            self.gameRound += 1
            
        loserIndex = (self.winnerIndex + 1) % 2
        
        print(f"\nThe duel ends after {self.gameRound} turns.")
        print(f"The mighty {self.players[self.winnerIndex].name} is victorious.")
        print(f"Sad clown {self.players[loserIndex].name} is weeping through layers of pie.")
        print("\nFinal positions:")
        print(self.players[0])
        print(self.players[1])
        
    def runOptimalStrategyGame(self):
        self.resetGame()
        
        self.players[0].position = self.minPos
        self.players[1].position = self.maxPos
        
        print ("*** CLOWN PIE DUEL ***")
        print (f"{self.players[0].name} vs. {self.players[1].name} square off,")
        print (f"  pies in hand, at {self.maxPos - self.minPos} paces.\n")
        
        print ("The duel begins...")
        
        while not self.gameOver:
            
            playerIndex = self.gameRound % 2
            opponentIndex = (playerIndex +  1) % 2
            
            player = self.players[playerIndex]
            opponent = self.players[opponentIndex]
            
            # see if we are at/past optimal strategy (sum of 1.0 aim chance), if so, fire
            totalChance = player.currentChance(opponent.position) + opponent.currentChance(player.position)
            #print (f"DEBUG: totalChance is {totalChance}")
            timeToFire = totalChance >= 1.0
            if timeToFire:
                
                print (f"\n{player.name} LAUNCHES A PIE!")
                print (f" ({player.name}'s odds of hitting are {player.currentChance(opponent.position)*100} %)")
                fireResult = player.fire(opponent.position)
                
                if True == fireResult:
                    print (f"{player.name} has hit their opponent.")
                    self.winnerIndex = playerIndex
                else:
                    print (f"{player.name} has missed their opponent.")
                    self.winnerIndex = opponentIndex
                self.gameOver = True
            else:
                stepIncrement = 1
                if playerIndex == 1:
                    stepIncrement = -1
                print(f"{player.name} takes a step forward.")
                player.step(stepIncrement)
                
            self.gameRound += 1
            
        loserIndex = (self.winnerIndex + 1) % 2
        
        print(f"\nThe duel ends after {self.gameRound} turns.")
        print(f"The mighty {self.players[self.winnerIndex].name} is victorious.")
        print(f"Sad clown {self.players[loserIndex].name} is weeping through layers of pie.")
        print("\nFinal positions:")
        print(self.players[0])
        print(self.players[1])
        