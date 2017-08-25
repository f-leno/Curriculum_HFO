#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 10:07:15 2017
Class to control tile coding defininitions
@author: Felipe Leno
"""
import Tiles.tiles as tiles
class TileManager():
    
    #Default parameters for tiles
    memct = 1024 #memory for hashtable
    numtilings = 5 #Number of tiles
    
    def get_tiles(self,state):
        """Transform a state composed of a group of continous features to tiles"""
        tiledState = tiles.tiles(self.numtilings,self.memct,state)
        #Converting to tuple makes the tile coding hashable
        return tuple(tiledState)
    
    