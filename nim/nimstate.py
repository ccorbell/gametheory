#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 11:42:41 2022

@author: Christopher Corbell

"""

class NimState:
    """
    A NimState is a specific game state (vertex of the game tree)
    in the game of Nim. 
    
    The game is represented as an array of non-negative integers. The 
    size of the array remains the same throughout a game, each position 
    representing a 'heap'. A move consists of subtracting some value
    from a single heap (array entry); at most the value itself (reducing
    it to zero).
    
    The game is over on the turn which reduces the final non-zero heap
    entry to zero.
    
    """
    def __init__(self, heaps:list):
        if None == heaps:
            raise Exception("heaps is a required parameter to NimState constructor")
        self.heaps = heaps
        self.heaps.sort()
        self.label = None
        self.alias = None
        
    def __repr__(self):
        rep = str(self.heaps)
        if not None == self.label:
            rep += f"\n({self.label})"
        
        if self.is_game_over():
            rep += " END"
        return rep
    
    def move(self, heap, count):
        """
        Perform a move by subtracting (count) items from a heap

        Parameters
        ----------
        heap : int
            The (zero-based) index of the heap from which to subtract.
        count : int
            The number of items to subtract from the indicated heap.

        Raises
        ------
        Exception
            This method will raise an exception for illegal moves,
            such as non-existant heap indexes, zero or negative count
            values, or count values which exceed the size of the heap.

        """
        if count < 1:
            raise Exception("Illegal move: at least one item must be removed")
            
        if heap < 0 or heap >= len(self.heaps):
            raise Exception(f"Illegal move; heap {heap} does not exist")
            
        oldval = self.heaps[heap]
        if count > oldval:
            raise Exception(f"Illegal move: at most {oldval} items can be removed from heap {heap}")
            
        self.heaps[heap] = oldval - count
        self.heaps.sort()
            
    def is_game_over(self):
        """
        Returns true if all heap counts are 0, false otherwise.

        """
        return self.heaps.count(0) == len(self.heaps)
    
    def get_ply(self):
        """
        Get the ply of this game state - this relies on label being
        dot-separated

        Returns
        -------
        The ply (game round) of this - 0 for root, 1 for player 1's first turn,
        2 for player 2's first turn, 3 for player 1's second turn, etc.

        """
        return self.label.count('.')
    
    def isPlayer1Outcome(self):
        return self.get_ply() % 2 == 1
    
    def isPlayer2Outcome(self):
        ply = self.get_ply()
        return ply > 0 and ply % 2 == 0
        
    def get_binary_heap_strings(self):
        """
        Get the current heap sizes as binary-encoded strings of a common length.

        Returns
        -------
        An array of strings representing binary encoding.

        """
        bstrings = []
        maxlen = 0
        for heap in self.heaps:
            bstring = f"{heap:b}"
            maxlen = max(maxlen, len(bstring))
            bstrings.append(bstring)
        #print(f"DEBUG: maxlen is {maxlen}")
        
        # add leading zeros so all are same length
        for n in range(0, len(bstrings)):
            zeros_to_prepend = maxlen - len(bstrings[n])
            if zeros_to_prepend > 0:
                newstring = ('0'*zeros_to_prepend) + bstrings[n]
                #print(f"DEBUG: newstring is {newstring}")
                bstrings[n] = newstring
                
        return bstrings
                
    def print_binary_table(self):
        """
        Print out the current set of heaps as a table of binary values

        Returns
        -------
        None.

        """
        heap_strings = self.get_binary_heap_strings()
        for heap_str in heap_strings:
            print (heap_str)
    
    def is_balanced(self):
        """
        Determine if the current game state is balanced.

        Returns
        -------
        True if the game state is balanced, false otherwise

        """
        return self.nim_sum() == 0
    
    def nim_sum(self):
        """
        Calculate the nim sum of the current state.

        Returns
        -------
        int

        """
        bstrings = self.get_binary_heap_strings()
        sumstring = ""
        for char_ix in range(0, len(bstrings[0])):
            ones_in_column = 0
            for str_ix in range(0, len(bstrings)):
                if bstrings[str_ix][char_ix] == '1':
                    ones_in_column += 1
            #print(f"DEBUG: in column {char_ix} there are {ones_in_column} ones")
            sumstring += f"{ones_in_column % 2}"
        #print(f"DEBUG: sumstring is {sumstring}")
        value = int(sumstring, 2)
        #print(f"DEBUG: value is {value}")
        return value
    
        