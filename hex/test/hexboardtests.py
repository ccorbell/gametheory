#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 13:40:59 2022

@author: Christopher Corbell
"""

import unittest

from hex.hexboard import HexBoard

def RunAllHexBoardTests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(HexBoardTests))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def Run1HexBoardTest(name):
    suite = unittest.TestSuite()
    suite.addTest(HexBoardTests(name))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def hexboardtests_main():
    unittest.main()
    
class HexBoardTests(unittest.TestCase):
    
    def testConstructor(self):
        hex3 = HexBoard(3)
        self.assertEqual(3, hex3.size)
        self.assertEqual(HexBoard.O_TOKEN, hex3.first_player)
        self.assertEqual(HexBoard.O_TOKEN, hex3.lr_player)
        
        hex5X = HexBoard(5, first_player=HexBoard.X_TOKEN)
        self.assertEqual(5, hex5X.size)
        self.assertEqual(HexBoard.X_TOKEN, hex5X.first_player)
        self.assertEqual(HexBoard.O_TOKEN, hex5X.lr_player)
        
    def testPlayAndGetTileValue(self):
        hex5 = HexBoard(5)
        
        for i in range(0, 5):
            for j in range(0, 5):
                self.assertEqual(HexBoard.EMPTY_TOKEN, hex5.getTileValue(i, j))
        
        hex5.playO(1,2)
        hex5.playX(4,4)
        hex5.playO(0,2)
        hex5.playX(3,4)
        
        self.assertEqual(HexBoard.O_TOKEN, hex5.getTileValue(1, 2))
        self.assertEqual(HexBoard.X_TOKEN, hex5.getTileValue(4, 4))
        self.assertEqual(HexBoard.O_TOKEN, hex5.getTileValue(0, 2))
        self.assertEqual(HexBoard.X_TOKEN, hex5.getTileValue(3, 4))
        
    def testBadPlayExeption(self):
        hex3 = HexBoard(3)
        
        with self.assertRaises(Exception):
            hex3.playO(-1, -1)
            
        with self.assertRaises(Exception):
            hex3.playX(3, 4)
        
    def testGetTilesOfValue(self):
        hex3 = HexBoard(3)
        hex3.playO(0,0)
        hex3.playX(2,2)
        hex3.playO(0,1)
        hex3.playX(0,2)
        hex3.playO(1,1)
        
        xtiles = hex3.getXTiles()
        self.assertEqual(2, len(xtiles))
        self.assertTrue([2,2] in xtiles)
        self.assertTrue([0,2] in xtiles)
        
        otiles = hex3.getOTiles()
        self.assertEqual(3, len(otiles))
        self.assertTrue([0,0] in otiles)
        self.assertTrue([0,1] in otiles)
        self.assertTrue([1,1] in otiles)
        
        empties = hex3.getEmptyTiles()
        self.assertEqual(4, len(empties))
        for xtile in xtiles:
            self.assertFalse(xtile in empties)
        for otile in otiles:
            self.assertFalse(otile in empties)
        self.assertTrue([1,0] in empties)
        self.assertTrue([1,2] in empties)
        self.assertTrue([2,0] in empties)
        self.assertTrue([2,1] in empties)
        
    def testAdjacent(self):
        self.assertTrue(HexBoard.adjacent([1,1], [1,2]))
        self.assertTrue(HexBoard.adjacent([1,1], [2,1]))
        
        self.assertTrue(HexBoard.adjacent([10,11], [10,12]))
        self.assertTrue(HexBoard.adjacent([8,10], [9,10]))
        
        self.assertTrue(HexBoard.adjacent([3,4], [2,5]))
        self.assertTrue(HexBoard.adjacent([3,4], [4,3]))
        
        self.assertFalse(HexBoard.adjacent([3,4], [4,5]))
        self.assertFalse(HexBoard.adjacent([3,4], [2,3]))
        
    def testGetConnectedBlocksAndWins(self):
        hex5 = HexBoard(5)
        
        hex5.playO(0,0)
        
        hex5.playX(2,0)
        
        hex5.playO(0,1)
        
        hex5.playX(2,1)
        
        hex5.playO(1,1)
        
        hex5.playX(2,2)
        
        hex5.playO(4,3)
        
        hex5.playX(2,3)
        
        hex5.playO(4,2)
        
        hex5.playX(3,3)
        
        hex5.playO(4,0)
        
        hex5.playX(2,4)
        
        expectedO1 = [[4, 0]]
        expectedO2 = [[4,2], [4,3]]
        expectedO3 = [[0,0], [0,1], [1,1]]
        
        oblocks = hex5.getConnectedOBlocks()
        self.assertEqual(3, len(oblocks))
        self.assertTrue(expectedO1 in oblocks)
        self.assertTrue(expectedO2 in oblocks)
        self.assertTrue(expectedO3 in oblocks)
        
        expectedX = [[2,0], [2,1], [2,2], [2,3], [2,4], [3,3]]
        expectedX.sort()
        
        xblocks = hex5.getConnectedXBlocks()
        self.assertEqual(1, len(xblocks))
        self.assertEqual(expectedX, xblocks[0])
        
        self.assertTrue(hex5.isXWin())
        self.assertFalse(hex5.isOWin())
        self.assertTrue(hex5.isGameOver())
        
        # if we switch X to playing left-to-right, it is no longer a win
        hex5.lr_player = HexBoard.X_TOKEN
        self.assertFalse(hex5.isXWin())
        self.assertFalse(hex5.isOWin())
        self.assertFalse(hex5.isGameOver())
    
if __name__ == "__main__":
    hexboardtests_main()
    