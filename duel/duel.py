#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 14:12:37 2022

@author: mathaes
"""

from duel.duelist import Duelist
from prob.pfunc import PFunc, LinearRangePFunc
import time

class Strategy:
    """
    A duel.Strategy dictates how players will decide to step vs. fire in a game.
    
    In optimal strategy, whenever sum of players' aim probabilities is 1 or greater,
    either player will choose to fire.
    
    In threshold strategy, each player has a (possibly different) probability
    threshold for when they will choose to fire.
    """

    # Type constants:
    OPTIMAL = 1 # fire when sum of aim probabiities is 1
    THRESHOLD = 2 # fire with per-player probability threshold is crossed
    
    def __init__(self, strategyType:int, 
                 player1value=None, 
                 player2value=None):
        self.type = strategyType
        self.player1value = player1value
        self.player2value = player2value
        
    def shouldFire(self, player1chance, player2chance, playerIndex):
        if self.type == Strategy.OPTIMAL:
            return player1chance + player2chance >= 1.0
        elif self.type == Strategy.THRESHOLD:
            if playerIndex == 0:
                return player1chance >= self.player1value
            elif playerIndex == 1:
                return player2chance >= self.player2value
    
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
                 player2func: PFunc = None,
                 verbose=True, # set true to see more game play-by-play
                 dramaTiming=True): # set true to see pauses in game output
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
        
        self.verbose = verbose
        self.dramaTiming = dramaTiming
        
    def resetGame(self):
        self.gameRound = 0
        self.players[0].position = 0
        self.players[1].position = self.maxPos
        self.gameOver = False
        
        
    def runGameWithStrategy(self, strategy):
        self.resetGame()
        
        self.players[0].position = self.minPos
        self.players[1].position = self.maxPos
        
        if self.verbose:
            print ("*** CLOWN PIE DUEL ***")
            print (f"{self.players[0].name} vs. {self.players[1].name} square off,")
            print (f"  pies in hand, at {self.maxPos - self.minPos} paces.\n")
            
            print ("The duel begins...")
        
        while not self.gameOver:
            
            
            playerIndex = self.gameRound % 2
            opponentIndex = (playerIndex +  1) % 2
            
            aimChances = [self.players[0].currentChance(self.players[1].position),
                          self.players[1].currentChance(self.players[0].position)]
            
            timeToFire = strategy.shouldFire(aimChances[0], aimChances[1], playerIndex)
            
            player = self.players[playerIndex]
            opponent = self.players[opponentIndex]
            
            if timeToFire:
                if self.verbose:
                    print (f"\n{player.name} LAUNCHES A PIE!")
                    print (f" ({player.name}'s chance of hitting is {player.currentChance(opponent.position)*100:.2f} %)\n")
                fireResult = player.fire(opponent.position)
                
                if self.dramaTiming:
                    time.sleep(0.5)
                    
                if True == fireResult:
                    if self.verbose:
                        print (f"{player.name} has hit their opponent.")
                    self.winnerIndex = playerIndex
                else:
                    if self.verbose:
                        print (f"{player.name} has missed their opponent.")
                    self.winnerIndex = opponentIndex
                
                if self.dramaTiming:
                    time.sleep(1)
                    
                self.gameOver = True
            else:
                stepIncrement = 1
                if playerIndex == 1:
                    stepIncrement = -1
                if self.verbose:
                    print(f"{player.name} takes a step forward.\n")
                    
                if self.dramaTiming:
                    time.sleep(0.5)
                    
                player.step(stepIncrement)
                
            self.gameRound += 1
            
        loserIndex = (self.winnerIndex + 1) % 2
        
        if self.verbose:
            print(f"\nThe duel ends after {self.gameRound} turns.")
            print(f"{self.players[self.winnerIndex].name} is victorious.")
            print(f"{self.players[loserIndex].name} is weeping through layers of pie.")
            print("\nFinal positions:")
            print(self.players[0])
            print(self.players[1])
            
        return {"winner": self.winnerIndex,
                "gameRound": self.gameRound}
    
        
    def runAimChanceThresholdGame(self, player1Threshold = 0.6, player2Threshold = 0.5):
        strategy = Strategy(Strategy.THRESHOLD, player1Threshold, player2Threshold)
        return self.runGameWithStrategy(strategy)
        
    def runOptimalStrategyGame(self):
        strategy = Strategy(Strategy.OPTIMAL)
        return self.runGameWithStrategy(strategy)
    
    def runAimThresholdStrategyTrials(self, 
                                      player1Threshold=0.6, 
                                      player2Threshold=0.5,
                                      numberOfTrials=1000):
        """
        Run a number of duels using the aim-threshold strategy.
        This turns off the verbose and dramaTiming flags, if set
        (and restores them afterward).

        Parameters
        ----------
        player1Threshold : float
            The aim probability threshold above which player 1 will fire.
        player2Threshold : float
            The aim probability threshold above which player 2 will fire.
        numberOfTrials : int, optional
            The number of trials to run. The default is 1000.

        Returns
        -------
        A dictionary with they keys:
            "count" - total duels run
            "player1wins" - total number of player 1 wins

        """
        wasVerbose = self.verbose
        wasDramaTiming = self.dramaTiming
        
        self.verbose = False
        self.dramaTiming = False
        
        count = 0
        player1wins = 0
        
        for n in range(0, numberOfTrials):
            results = self.runAimChanceThresholdGame(player1Threshold, player2Threshold)
            if results["winner"] == 0:
                player1wins += 1
            count += 1
            
        self.verbose = wasVerbose
        self.dramaTiming = wasDramaTiming
        return {"count":count, "player1wins":player1wins}
    
    def runOptimalStrategyTrials(self, numberOfTrials=1000):
        """
        Run a number of duels using the optimal strategy.
        This turns off the verbose and dramaTiming flags, if set
        (and restores them afterward).

        Parameters
        ----------
        numberOfTrials : TYPE, optional
            DESCRIPTION. The default is 1000.

        Returns
        -------
        A dictionary with they keys:
            "count" - total duels run
            "player1wins" - total number of player 1 wins

        """
        wasVerbose = self.verbose
        wasDramaTiming = self.dramaTiming
        
        self.verbose = False
        self.dramaTiming = False
        
        count = 0
        player1wins = 0
        
        for n in range(0, numberOfTrials):
            results = self.runOptimalStrategyGame()
            if results["winner"] == 0:
                player1wins += 1
            count += 1
            
        self.verbose = wasVerbose
        self.dramaTiming = wasDramaTiming
        return {"count":count, "player1wins":player1wins}
    
    
        