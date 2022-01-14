#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 14:11:39 2022

@author: Christopher Corbell
"""

import copy

class Board:
    """
    Representation of a tic-tac-toe board, in a particular state.
    
    The board is represented internally as an array of 9 characters with  
    indexes corresponding to board grid positions as follows:
        
     012
     349
     678
    
    Values are represented as 'X', 'O', or '-' (unset)
    
    The board supports label and alias fields. A label is typically a
    unique string. An alias refers to another (isomorphic) board's label.
    
    The board has makeCanonical() method which will rotate/reflect the
    board to a canonical form. Two isomorphic boards will have the same
    canonical forms, which can be quickly affirmed by comparing lexicalString()
    output values. (Boards that are not made canonical can produce canonical
    lexical strings via the canonicalString() function.)
    
    The methods xplay() and oplay() can be used to make a new play
    to a board. By default these methods will validate that the move is legal.
    (For example, they prevent X or O from playing twice in a row, or
    playing on an already-played position). These methods will also detect
    and automatically set a .block flag on the board if a play blocks the opposing
    player's win. (Subsequent plays on the same board will clear this flag).
    """
    GRID_SIZE = 3*3
    
    EMPTY_TOKEN = '-'
    X_TOKEN = 'X'
    O_TOKEN = 'O'

    
    WIN_SETS = [{0, 1, 2}, 
                {3, 4, 5}, 
                {6, 7, 8}, 
                {0, 3, 6}, 
                {1, 4, 7}, 
                {2, 5, 8}, 
                {0, 4, 8}, 
                {6, 4, 2}]
    
    def __init__(self):
        self.grid = ['-'] * 9
        self.label = None
        self.alias = None
        self.block = False # is this board a win-block?
        
    def prettyValue(self, index):
        if self.grid[index] == Board.EMPTY_TOKEN:
            return ' '
        return self.grid[index]
    
    def __repr__(self):
        
        
        s = self.prettyValue(0) + '|' + self.prettyValue(1) + '|' + self.prettyValue(2)
        s += '\n'
        s += '-' * 5
        
        s += '\n'
        s += self.prettyValue(3) + '|' + self.prettyValue(4) + '|' + self.prettyValue(5) +'\n'
        s += '-' * 5
        s += '\n'
        s += self.prettyValue(6) + '|' + self.prettyValue(7) + '|' + self.prettyValue(8)
        
        if not None == self.label:
            s += f"\n({self.label})"
        
        if not None == self.alias:
            s += f"\n≅({self.alias})"
            
        if self.isWin():
            s += f"\n{self.winString()}"
        elif self.isDraw():
            s += "\nDraw"
        elif self.block:
            s += f" \n{self.lastPlayer()} blocks {self.nextPlayer()}"
        
        return s
    
    
    def __copy__(self):
        c = Board()
        c.grid = self.grid[:]
        c.label = self.label
        c.alias = self.alias
        c.block = self.block
        return c
        
    def __deepcopy__(self):
        c = Board()
        c.grid = self.grid[:]
        c.label = self.label
        c.alias = self.alias
        c.block = self.block
        return c
    
    def copy(self):
        return copy.copy(self)
    
    def lastPlayer(self):
        """
        Determines the player who brought this board to its current state.

        Returns the player token, or None if this board is empty.
        -------
        String (or None)
            'X' if X gets made the last move, 'O' if O made the last move,
            None if this board is empty or in a bad state.

        """
        xcount = self.X_count()
        ocount = self.O_count()
        if xcount + ocount == 0:
            return None
        
        if xcount == ocount:
            return Board.O_TOKEN
        elif xcount == ocount + 1:
            return Board.X_TOKEN
        
        return None # bad state
        
    def nextPlayer(self):
        """
        Return which player gets the next move from this board.

        Returns
        -------
        String (or None)
            'X' if X gets the next move, 'O' if O gets the next move,
            None if there are no moves remaining in the board

        """
        xcount = self.X_count()
        ocount = self.O_count()
        if xcount + ocount >= 9:
            return None
        
        if xcount == ocount:
            return Board.X_TOKEN
        elif xcount == ocount + 1:
            return Board.O_TOKEN
        else:
            raise Exception(f"Board in bad state, {xcount} X entries and {ocount} O entries:\n{self}")
    
    def xplay(self, index, enforceLegalMove=True, markBlock=True):       
        if index < 0 or index >= Board.GRID_SIZE:
            raise Exception(f"index {index} out of bounds for 3x3 grid")
        
        if enforceLegalMove:
            if self.isWin():
                raise Exception(f"Invalid move; this board is already a {self.winString()}")
                
            if self.nextPlayer() != Board.X_TOKEN:
                raise Exception(f"Invalid board state for X to play:\n{self}")
            
            if self.grid[index] != Board.EMPTY_TOKEN:
                raise Exception(f"Invalid move; board entry {index} is not empty:\n{self}")
            
        self.block = False
        if markBlock:
            # is this play blocking a win for O?
            testWin = self.O_indices()
            testWin.append(index)
            for winset in Board.WIN_SETS:
                if winset.issubset(testWin):
                    self.block = True
                    
        self.grid[index] = Board.X_TOKEN
        
    def oplay(self, index, enforceLegalMove=True, markBlock=True):
        if index < 0 or index >= Board.GRID_SIZE:
            raise Exception(f"index {index} out of bounds for 3x3 grid")
        
        if enforceLegalMove:
            if self.isWin():
                raise Exception(f"Invalid move; this board is already a {self.winString()}")
                
            if self.nextPlayer() != Board.O_TOKEN:
                raise Exception(f"Invalid board state for X to play:\n{self}")
                
            if self.grid[index] != Board.EMPTY_TOKEN:
                raise Exception(f"Invalid move; board entry {index} is not empty:\n{self}")
                
        self.block = False
        if markBlock:
            # is this play blocking a win for X?
            testWin = self.X_indices()
            testWin.append(index)
            for winset in Board.WIN_SETS:
                if winset.issubset(testWin):
                    self.block = True
            
        self.grid[index] = Board.O_TOKEN
        
    def X_count(self):
        return self.grid.count(Board.X_TOKEN)
        
    def O_count(self):
        return self.grid.count(Board.O_TOKEN)
    
    def ply_count(self):
        return self.X_count() + self.O_count()
        
    def empty_count(self):
        return self.grid.count(Board.EMPTY_TOKEN)
    
    def empty_indices(self):
        return list(filter(lambda i: self.grid[i]==Board.EMPTY_TOKEN, range(len(self.grid))))
        
    def X_indices(self):
        return list(filter(lambda i: self.grid[i]==Board.X_TOKEN, range(len(self.grid))))
    
    def O_indices(self):
        return list(filter(lambda i: self.grid[i]==Board.O_TOKEN, range(len(self.grid))))
        
    def isXWin(self):
        xiset = set(self.X_indices())
        if len(xiset) < 3:
            return False
        
        for winset in Board.WIN_SETS:
            if winset.issubset(xiset):
                return True
            
        return False
    
    def isOWin(self):
        oiset = set(self.O_indices())
        if len(oiset) < 3:
            return False
        
        for winset in Board.WIN_SETS:
            if winset.issubset(oiset):
                return True
            
        return False
    
    def isWin(self):
        return self.isXWin() or self.isOWin()
    
    def winString(self):
        if self.isXWin():
            return "win for X"
        elif self.isOWin():
            return "win for O"
        return ''
    
    def isDraw(self):
        
        if self.empty_count() == 0:
            return not self.isWin()
        
        # TODO - add logic to determine if a draw is inevitable 
        # before the ninth ply? This can be shown if only isolated
        # empty squares remain and no remaining plays can create a win from them.
        
        return False
        
    def reflect(self):
        """
        Reflect the board entries around the vertical axis.

        Returns
        -------
        None.

        """
        tempgrid = self.grid.copy()
        self.grid[0] = tempgrid[2]
        self.grid[2] = tempgrid[0]
        self.grid[3] = tempgrid[5]
        self.grid[5] = tempgrid[3]
        self.grid[6] = tempgrid[8]
        self.grid[8] = tempgrid[6]
        del tempgrid
    
    def rotate(self):
        """
        Rotate the board entries 90 degrees (counter-clockwise).

        Returns
        -------
        None.

        """
        tempgrid = self.grid.copy()
        self.grid[0] = tempgrid[2]
        self.grid[1] = tempgrid[5]
        self.grid[2] = tempgrid[8]
        self.grid[3] = tempgrid[1]
        self.grid[5] = tempgrid[7]
        self.grid[6] = tempgrid[0]
        self.grid[7] = tempgrid[3]
        self.grid[8] = tempgrid[6]
        del tempgrid
        
    def lexstring(self):
        """
        Return a lexical string representation of this board.
        This is simply a concatenation of the 9 grid char values.
        Note this differs from str() or __repr__, which produce a
        representation with newlines suitable for printing to the screen.

        Returns
        -------
        String
            A String representation of this board's grid suited for 
            lexical comparisons.

        """
        return "".join(self.grid)
    
    def canonicalString(self):
        """
        Find the canonical string representation of this board.
        This method gets the lexstring representation of all possible
        rotations and reflections of this board, sorts them lexically,
        and returns the first such lexstring.
        
        Note, this does not change this board; use makeCanonical to
        convert this board to canonical ordering.

        Returns
        -------
        String
            The canonical lexstring representation of this board.

        """
        lexstrings = []
        maker = Board()
        maker.grid = self.grid.copy()
        lexstrings.append(maker.lexstring())
        for n in range(0, 3):
            maker.rotate()
            lexstrings.append(maker.lexstring())
        maker.reflect()
        lexstrings.append(maker.lexstring())
        for n in range(0, 3):
            maker.rotate()
            lexstrings.append(maker.lexstring())
        # the canonical string is the rotation/reflection
        # which lexically sorts last
        lexstrings.sort()
        return lexstrings.pop()
    
    def makeCanonical(self):
        """
        Convert this board's grid to canonical rotation/reflection.
        This uses canonicalString to find the initial lexical sort
        based on character representation, then assigns the grid
        based on the canonical string.

        Returns
        -------
        None.

        """
        canstr = self.canonicalString()
        self.grid = list(canstr)
        
    def isIsomorphic(self, otherBoard):
        """
        Determine if this board is isomorphic to another board.
        Note that is you call makeCanonical() on both boards first you
        don't need this method, just compare lexstring() values.

        Parameters
        ----------
        otherBoard : Board
            Another tttoe Board

        Returns
        -------
        bool
            True if the two boards are isomorphic, False otherwise.

        """
        # fast up front checks
        if self.grid == otherBoard.grid:
            return True
        
        if self.X_count() != otherBoard.X_count():
            return False
        if self.O_count() != otherBoard.O_count():
            return False
        if self.grid[4] != otherBoard.grid[4]:
            return False
        
        can1 = self.canonicalString()
        can2 = otherBoard.canonicalString()
        return can1 == can2

        