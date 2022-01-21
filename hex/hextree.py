#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 12:45:15 2022

@author: Christopher Corbell
"""

from hex.hexboard import HexBoard

class HexTree:
    
    def __init__(self):
        self.plies = []
        
    def generateChildBoards(parent: HexBoard, assignLabels=True):
        nextPlayer = parent.getNextPlayer()
        if nextPlayer == HexBoard.EMPTY_TOKEN:
            raise Exception("Can't generate child boards, this board is game-over or in unexpected state")
            
        emptyTiles = parent.getEmptyTiles()
        childBoards = []
        n = 0
        for tile in emptyTiles:
            childBoard = parent.copy()
            if nextPlayer == HexBoard.X_TOKEN:
                childBoard.playX(tile[0], tile[1])
            else:
                childBoard.playO(tile[0], tile[1])
                
            if assignLabels:
                childBoard.label = parent.label + f".{n}"
                n += 1
            childBoards.append(childBoard)
        return childBoards
    
    def generateTree(self, root:HexBoard, maxDepth=-1):
        self.plies = []
        
        depth = 0
        lastPly = [root]
        currentPly = []
        
        if maxDepth == -1:
            maxDepth = root.countEmptyTiles()
            
        while depth < maxDepth:
            for parent in lastPly:
                if parent.isGameOver():
                    continue
                children = HexTree.generateChildBoards(parent)
                currentPly.extend(children)
            
            self.plies.append(currentPly)
            lastPly = currentPly
            currentPly = []
            depth += 1
        
    def generateBoardFromLabel(label, root):
        boards = HexTree.getAllBoardsForLabel(label)
        if len(boards) == 0:
            return None
        return boards.pop()
    
        
    def getAllBoardsForLabel(label, root):
        
        labelParts = label.split('.')
        currentLabel = labelParts[0]
        root.label = currentLabel
        
        results = [root]
        nextRoot = root
        
        for index in range(1, len(labelParts)):
            
            nextIndex = int(labelParts[index])
            currentLabel += f".{labelParts[index]}"
            
            children = HexTree.generateChildBoards(nextRoot)
            if nextIndex < 0 or nextIndex >= len(children):
                raise Exception(f"Could not get object for label {currentLabel} - bad index")
            
            nextRoot = children[nextIndex]
            nextRoot.label = currentLabel
            results.append(nextRoot)
        
        return results
    
    def findWins(root, forPlayer=HexBoard.O_TOKEN, labelsOnly=False):
        """
        Given a root hex board, find all winning boards for
        a player (token), or for either player if forPlayer is
        None or empty.
        
        The method returns a list of winning boards, unless
        labelsOnly is set to True.
        
        The boards are found in a breadth-first generative search
        of the game tree below root.

        Parameters
        ----------
        root : HexBoard
            A valid HexBoard, canonically labeled.

        Returns
        -------
        A list of winning HexBoard objects, unless labelsOnly=True,
        then this method returns a list of label strings.
        """
        resultBoards = []
        resultLabels = []
        children = HexTree.generateChildBoards(root)
        for child in children:
            childIsLeaf = child.isGameOver()
            childIsWin = False
            
            if forPlayer == HexBoard.O_TOKEN:
                childIsWin = child.isOWin()
            elif childIsWin == HexBoard.X_TOKEN:
                childIsWin == child.isXWin()
            else:
                childIsWin = childIsLeaf
            
            if childIsWin:
                if labelsOnly:
                    resultLabels.append(child.label)
                else:
                    resultBoards.append(child)
                    
            if not childIsLeaf:
                
                childWins = HexTree.findWins(child, forPlayer, labelsOnly)
                if labelsOnly:
                    resultLabels.extend(childWins)
                else:
                    resultBoards.extend(childWins)
        
        if labelsOnly:
            return resultLabels
        else:
            return resultBoards
    
        