#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 12:44:53 2022

@author: mathaes
"""
import copy

class HexBoard:
    """
    The HexBoard class represents a state of a game of Hex on an
    n x n hexagonal-parallelogram board. 
    
    The two players are represented by X and O.
    
    One player plays in the left-right (across columns) and
    the other in the top-bottom (across rows).  These can
    be changed but the default is that O plays first, in left-right direction.
    """
    
    EMPTY_TOKEN = '-'
    X_TOKEN = 'X'
    O_TOKEN = 'O'
    
    def __init__(self, 
                 size=11, 
                 first_player = O_TOKEN, 
                 lr_player = O_TOKEN):
        self.size = size
        self.first_player = first_player
        self.lr_player = lr_player
        self.label = '0'
        self.clear()
    
        
    def __repr__(self):
        strrep = ''
        for row in range(0, self.size):
            if row == int(self.size / 2):
                strrep += self.lr_player
                strrep += ' ' * (row)
            else:
                strrep += ' ' * (row + 1)
                
            for col in range(0, self.size):
                curValue = self.getTileValue(row, col)
                strrep += curValue
                if col < self.size - 1:
                    strrep += ' '
                    
            strrep += '\n'
            
        if None != self.label:
            strrep += f"({self.label})\n"
                
        return strrep
    
    def __copy__(self):
        clone = HexBoard()
        clone.size = self.size
        clone.first_player = self.first_player
        clone.lr_player = self.lr_player
        clone.board = copy.deepcopy(self.board)
        clone.label = self.label
        return clone
        
    def copy(self):
        return copy.copy(self)
    
    def getTileValue(self, row, col):
        if row < 0 or col < 0 or row >= self.size or col >= self.size:
            raise Exception(f"Coordinate ({row},{col}) is out of range for this board.")
        
        return self.board[row][col]
    
    def playX(self, row, col):
        if self.getNextPlayer() != self.X_TOKEN:
            raise Exception("playX called but next player is not X")
            
        cur = self.getTileValue(row, col)
        if not HexBoard.EMPTY_TOKEN == cur:
            raise Exception(f"Coordinate ({row},{col}) is {cur} (not unset).")
        
        self.board[row][col] = HexBoard.X_TOKEN
    
    def playO(self, row, col):
        if self.getNextPlayer() != self.O_TOKEN:
            raise Exception("playX called but next player is not X")
            
        cur = self.getTileValue(row, col)
        if not HexBoard.EMPTY_TOKEN == cur:
            raise Exception(f"Coordinate ({row},{col}) is {cur} (not unset).")
        
        self.board[row][col] = HexBoard.O_TOKEN
        
    def getSelfPlayer(self):
        """
        Determine which player played last for the current board state.

        Returns
        -------
        Either TOKEN_X or TOKEN_O, unless the board is empty 
        in which case it returns TOKEN_EMPTY

        """
        xcount = self.countXTiles()
        ocount = self.countOTiles()
        
        if self.first_player == HexBoard.O_TOKEN:
            if xcount == ocount:
                return HexBoard.X_TOKEN
            elif xcount == ocount-1:
                return HexBoard.O_TOKEN
            else:
                raise Exception(f"Bad board state: O goes first but there are {ocount} O tiles and {xcount} X tiles")

        elif self.first_player == HexBoard.X_TOKEN:
            if xcount == ocount:
                return HexBoard.O_TOKEN
            elif ocount == xcount-1:
                return HexBoard.X_TOKEN
            else:
                raise Exception(f"Bad board state: X goes first but there are {ocount} O tiles and {xcount} X tiles")
                
        return HexBoard.EMPTY_TOKEN
        
    def getNextPlayer(self):
        """
        Determine which player plays next from the current board state.

        Returns
        -------
        Either TOKEN_X or TOKEN_O, unless the game is over
        in which case it returns TOKEN_EMPTY

        """
        if self.isGameOver():
            return HexBoard.EMPTY_TOKEN
        cur = self.getSelfPlayer()
        if cur == HexBoard.O_TOKEN:
            return HexBoard.X_TOKEN
        elif cur == HexBoard.X_TOKEN:
            return HexBoard.O_TOKEN
        
        return HexBoard.EMPTY_TOKEN
    
    def clear(self):
        self.board = []
        for n in range(0, self.size):
            self.board.append([HexBoard.EMPTY_TOKEN] * self.size)
            
    def getTileCoordinatesOfValue(self, value):
        coords = []
        for i in range(0, self.size):
            for j in range(0, self.size):
                cur = self.getTileValue(i, j)
                if cur == value:
                    coords.append([i, j])
        return coords
    
    def countXTiles(self):
        return self.countTiles(HexBoard.X_TOKEN)
    
    def countOTiles(self):
        return self.countTiles(HexBoard.O_TOKEN)
    
    def countEmptyTiles(self):
        return self.countTiles(HexBoard.EMPTY_TOKEN)
    
    def countTiles(self, value):
        count = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                cur = self.getTileValue(i, j)
                if cur == value:
                    count += 1
        return count
    
    def getXTiles(self):
        return self.getTileCoordinatesOfValue(HexBoard.X_TOKEN)
    
    def getOTiles(self):
        return self.getTileCoordinatesOfValue(HexBoard.O_TOKEN)
    
    def getEmptyTiles(self):
        return self.getTileCoordinatesOfValue(HexBoard.EMPTY_TOKEN)
    
    def adjacent(tile1, tile2):
        rowDiff = tile1[0] - tile2[0]
        colDiff = tile1[1] - tile2[1]
        rowAdjacent = rowDiff == 0 and abs(colDiff) == 1
        colAdjacent = colDiff == 0 and abs(rowDiff) == 1
        diagAdjacent = abs(rowDiff) == 1 and rowDiff + colDiff == 0
        return rowAdjacent or colAdjacent or diagAdjacent
    
    def adjacentIndexes(tile, tileArray):
        indexes = []
        for n in range(0, len(tileArray)):
            if HexBoard.adjacent(tile, tileArray[n]):
                indexes.append(n)
        return indexes
        
    def getConnectedOBlocks(self):
        return HexBoard.getBlocks(self.getOTiles())
    
    def getConnectedXBlocks(self):
        return HexBoard.getBlocks(self.getXTiles())
    
    def getBlocks(tiles):
        """
        Given a set of tiles, return them partitioned into
        blocks of adjacent tiles

        Parameters
        ----------
        tiles : list
            A list of tile coordinates

        Returns
        -------
        blocks : list of lists
            A list coordinate-list blocks, where each block
            is a group of connected coordinates (by hexagonal adjacency)
        """
        blocks = []
        while len(tiles) > 0:
            nextTile = tiles.pop(0)
            block = HexBoard.recursiveAdjacencies(nextTile, tiles)
            block.append(nextTile)
            block.sort()
            blocks.append(block)            
        
        return blocks
    
    def recursiveAdjacencies(tile, tileArray):
        adjacencies = []
        adjixs = HexBoard.adjacentIndexes(tile, tileArray)
        if len(adjixs) == 0:
            return []
        
        adjixs.sort()
        adjixs.reverse()
        subtiles = []
        
        for ix in adjixs:
            subtile = tileArray.pop(ix)
            subtiles.append(subtile)
        adjacencies.extend(subtiles)
        
        for sub in subtiles:
            more = HexBoard.recursiveAdjacencies(sub, tileArray)
            if len(more) > 0:
                adjacencies.extend(more)
                
        return adjacencies
    
    def isXWin(self):
        check_lr = self.lr_player == HexBoard.X_TOKEN
        xblocks = self.getConnectedXBlocks()
        for xblock in xblocks:
            if check_lr:
                if self.block_spans_lr(xblock):
                    return True
            else:
                if self.block_spans_tb(xblock):
                    return True
        
        return False
    
    def isOWin(self):
        check_lr = self.lr_player == HexBoard.O_TOKEN
        oblocks = self.getConnectedOBlocks()
        for oblock in oblocks:
            if check_lr:
                if self.block_spans_lr(oblock):
                    return True
            else:
                if self.block_spans_tb(oblock):
                    return True
        
        return False
    
    def block_spans_lr(self, block):
        # we assume the block is connected, so we
        # just look for an element with 0 first entry
        # and one with size-1 first entry
        foundLeft = False
        foundRight = False
        for coord in block:
            if coord[0] == 0:
                foundLeft = True
            elif coord[0] == self.size - 1:
                foundRight = True
            if foundLeft and foundRight:
                return True
            
        return False
    
    def block_spans_tb(self, block):
        # we assume the block is connected, so we
        # just look for an element with 0 first entry
        # and one with size-1 first entry
        foundTop = False
        foundBottom = False
        for coord in block:
            if coord[1] == 0:
                foundTop = True
            elif coord[1] == self.size - 1:
                foundBottom = True
            if foundTop and foundBottom:
                return True
            
        return False
    
    def isGameOver(self):
        if self.countEmptyTiles() == 0:
            return True
        
        return self.isXWin() or self.isOWin()
    
    
    
    
    