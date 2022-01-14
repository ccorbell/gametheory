#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 10:43:00 2022

@author: Christopher Corbell
"""

from tttoe.board import Board

class GameTree:
    """
    A GameTree can generate a tree of tic tac toe Board nodes.
    The tree is generate as tiers of boards at each ply.
    Boards are labeled to indicate their paths through the tree.
    
    Board 'aliases' can be used to prune isomorphic subtrees
    that arise from different parents at the same play;
    only one of such isomorphs is continued, the others have
    their .alias field set to the label of that one for reference.
    This is optional behavior; set 'skipAliases' to True in
    the generateTree() call to identify and skip such isomorphs.
    
    (Note that isomorphic children of the -same- parent board are always
     skipped, only unique children of each parent are considered)
    """
    def __init__(self, rootBoard:Board=None):
        if None == rootBoard:
            self.root = Board()
            self.root.label = '0'
            self.plies = []
        else:
            self.root = rootBoard
            self.plies = []
            
    def generateTree(self, skipAliases:bool):
        
        lastPly = [self.root]
        currentPly = []
        
        depth = 0
        while depth < 9:

            for parent in lastPly:
                if True == skipAliases:
                    if not (None == parent.alias):
                        print (f"skipping parent {parent.label}, alias of {parent.alias}...")
                        continue
                
                if parent.isWin():
                    print (f"skipping parent {parent.label}, {parent.winString()}")
                    continue
                
                #if parent.isDraw():
                #    continue
                children = GameTree.generateChildBoards(parent)
                print (f"...generated {len(children)} child boards from parent {parent.label}")
                currentPly.extend(children)
            
            if skipAliases:
                GameTree.determineAliases(currentPly)
                
            self.plies.append(currentPly)
            lastPly = currentPly
            currentPly = []
            depth += 1
        
    
    def print_tree_size(self):
        totalSize = 1
        for n in range(0, len(self.plies)):
            print(f"ply {n+1} size: {len(self.plies[n])}")
            totalSize += len(self.plies[n])

        print(f"total tree size (including root, excluding isomorphic branches): {totalSize}")
        
    def print_tree(self):
        print (self.root)
        
        for n in range(0, len(self.plies)):
            print ('===========================================')
            print (f'ply {n+1}:')
            for board in self.plies[n]:
                print (board)
                print('')
            
    def print_ply(self, index):
        if index == 0:
            print ('=========================================== 1 board at root')
            print (f"{self.root}\n")
        else:
            print (f'=========================================== {len(self.plies[index-1])} boards in ply {index}')
            for board in self.plies[index - 1]:
                print(f"{board}\n")
            
    def generateChildBoards(parent: Board):
        """
        Given a parent game board, generate all of its next-move boards
        up to isomorphism. Boards are canonical and are labeled
        with increasing integers appended to the parent label.
        For example, if parent is labeled '0.3' and there are 4 child
        boards, they will be labeled '0.3.0, '0.3.1', 0.3.2', 0.3.3'.

        Parameters
        ----------
        parent : Board
            A parent board.

        Returns
        -------
        childBoards : [Board]
            A list of all possible child boards (next plays of the game
            from the parent board state) up to isomorphism.

        """
        childBoardCanonicalStrings = []
        blocks = set()
        
        isPlayingX = parent.nextPlayer() == Board.X_TOKEN
        emptyIndices = parent.empty_indices()
 
        for playIndex in emptyIndices:
            childBoard = parent.copy()
            if isPlayingX:
                childBoard.xplay(playIndex)
            else:
                childBoard.oplay(playIndex)
                
            childStr = childBoard.canonicalString()
            if childBoard.block:
                blocks.add(childStr)
            if not childStr in childBoardCanonicalStrings:
                childBoardCanonicalStrings.append(childStr)
            del childBoard
        
        childBoards = []
        index = 0
        for gridString in childBoardCanonicalStrings:
            child = Board()
            child.grid = list(gridString)
            child.label = parent.label + "." + str(index)
            if gridString in blocks:
                print(f"- block played in board {child.label}")
                child.block = True
            index += 1
            childBoards.append(child)
        return childBoards
    
    def determineAliases(plyboards):
        """
        Given a list of child-board lists of the same ply,
        determine aliases of isomorphic boards. This assumes
        all boards are already canonical so we can simply compare
        lexical string representation.
        
        As a subtle improvement, we use the block property of
        each board to prefer blocks as alias targets (so continuing
        isomorphic branches explicitly have blocking plays as parent nodes)
        (A block is a play which removes a winning next-move opportunity)

        Parameters
        ----------
        childBoardLists : [[Board]]
            A list of Board lists, expected to be returned by
            generateChildBoards for the same ply level (game-tree depth)

        Returns
        -------
        None; alias value is set on Board objects passed in

        """
        
        # resolve aliases to block-play boards first
        block_indices = [idx for idx, element in enumerate(plyboards) if element.block]
        for block_index in block_indices:
            target = plyboards[block_index]
            for otherIndex in range(0, len(plyboards)):
                if otherIndex in block_indices:
                    continue
                
                other = plyboards[otherIndex]
                if not None == other.alias: # already determined
                    continue
                if target.lexstring() == other.lexstring():
                    other.alias = target.label
                    
        # now resolve everything else
        targetIndex = 0
        for targetIndex in range(0, len(plyboards) - 1):
            target = plyboards[targetIndex]
            if target.block: # already processed
                continue
            if not None == target.alias: # already determined to be alias
                continue
            
            for laterIndex in range(targetIndex+1, len(plyboards)):
                later = plyboards[laterIndex]
                if not None == later.alias: # already determined
                    continue
                if target.lexstring() == later.lexstring():
                    # found an alias
                    later.alias = target.label
