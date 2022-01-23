#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 16:34:58 2022

@author: Christopher Corbell
"""

import random

class Deck:
    
    SUITS = ['S', 'H', 'C', 'D']
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8','9', '10', 'J', 'Q', 'K']
    
    def makeDeck(ranks, suits):
        deck = []
        for suit in suits:
            for rank in ranks:        
                card = rank + suit
                deck.append(card)
        return deck
    
    STANDARD_DECK = makeDeck(RANKS, SUITS)
    
    def __init__(self, cards=STANDARD_DECK):
        self.cards = cards
        self.dealt = []
        
    def __repr__(self):
        if len(self.dealt) == 0:
            return f"cards:{self.cards}\n"
        
        return f"cards:{self.cards}\ndealt:{self.dealt}\n"
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    def reset(self):
        self.cards.extend(self.dealt)
        self.dealt = []
        self.shuffle()
        
    def shuffleDealtAndAppend(self):
        random.shuffle(self.dealt)
        self.cards.extend(self.dealt)
        self.dealt = []

    def deal(self, count):
        hand = []
        for n in range(0, count):
            card = self.cards.pop(0)
            hand.append(card)
            self.dealt.append(card)
        return hand