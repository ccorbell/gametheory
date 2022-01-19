#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 11:59:03 2022

@author: Christopher Corbell
"""

from nim.nimstate import NimState

class NimTree:
    
    def __init__(self):
        self.plies = []
        self.states_by_label = {}
        self.leaf_nodes = []
    
    def generateChildStates(self, parent: NimState):
        childStates = []
        
        heapIndices = []
        for n in range(0, len(parent.heaps)):
            if parent.heaps[n] > 0:
                heapIndices.append(n)
                
        heapCheck = []
        
        print (f"DEBUG: heapIndices: {heapIndices}")
        for heapIndex in heapIndices:
            print(f"DEBUG parent: {parent}")
            heapSize = parent.heaps[heapIndex]
            for amount in range(1, heapSize+1):
                child = NimState(heaps=parent.heaps.copy())
                print(f"DEBUG: removing amount {amount} from index {heapIndex}; child: {child}")
                child.move(heapIndex, amount)
                if not child.heaps in heapCheck:
                    childStates.append(child)
                    heapCheck.append(child.heaps.copy())
                    print(f"DEBUG child: {child}")
        
        for i in range(0, len(childStates)):
            childStates[i].label = f"{parent.label}.{i}"
            
        return childStates
          
    def gameOverInAllStates(self, states):
        for state in states:
            if False == state.is_game_over():
                return False
        return True
    
    def generateGameTree(self, initialState: NimState):
        if None == initialState.label:
            initialState.label = '0'
        
        currentPly = [initialState]
        self.plies = [currentPly]
        self.states_by_label = {initialState.label:initialState}
        self.leaf_nodes = []
        
        while not self.gameOverInAllStates(currentPly):
            parentPly = currentPly
            currentPly = []
            for parent in parentPly:
                children = self.generateChildStates(parent)
                currentPly.extend(children)
                for child in children:
                    self.states_by_label[child.label] = child
                    if child.is_game_over():
                        self.leaf_nodes.append(child)
                        
            self.plies.append(currentPly)

    def print_ply(self, plyIndex):
        if plyIndex < 0 or plyIndex >= len(self.plies):
            raise Exception(f"Bad ply index: {plyIndex}")
        
        for state in self.plies[plyIndex]:
            print(f"{state}\n")
            
    def get_leaf_states(self):
        return self.leaf_nodes
    
    def get_leaf_labels(self):
        return [node.label for node in self.leaf_nodes]
    
    def get_leaf_labels_player1(self):
        p1leaves = filter(lambda node: node.isPlayer1Outcome(), self.leaf_nodes)
        return [leaf.label for leaf in p1leaves]
    
    def get_leaf_labels_player2(self):
        p1leaves = filter(lambda node: node.isPlayer2Outcome(), self.leaf_nodes)
        return [leaf.label for leaf in p1leaves]
    
    def get_leaf_labels_of_ply(self, ply):
        plyLeaves = filter(lambda node: node.get_ply() == ply, self.leaf_nodes)
        return [leaf.label for leaf in plyLeaves]
        
    def get_state_by_label(self, label):
        if label in self.states_by_label:
            return self.states_by_label[label]
        return None
    
    def get_game_sequence(self, leaf_label):
        sequence = []
        
        label_parts = leaf_label.split('.')
        fetch_label = ''
        for n in range(0, len(label_parts)):
            fetch_label += label_parts[n]
            next_state = self.get_state_by_label(fetch_label)
            if None == next_state:
                raise Exception(f"get_game_sequence failed to retrieve state for label {fetch_label}")
            sequence.append(next_state)
            fetch_label += '.'
        return sequence
    
