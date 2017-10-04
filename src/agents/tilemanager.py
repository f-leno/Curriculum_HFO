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
    memct = 48 #memory for hashtable
    numtilings = 5 #Number of tiles
    
    def get_tiles(self,state):
        """Transform a state composed of a group of continous features to tiles"""
        tiledState = tiles.tiles(self.numtilings,self.memct,state)
        #Converting to tuple makes the tile coding hashable
        return tuple(tiledState)
    

import math
class TileCoding():
    upperBoundVariable = None    
    lowerBoundVariable = None
    t = None
    w = None
    tileList = []
    def __str__(self):
        return "TileCoding. Params: UpperBoundVariable: "+str(self.upperBoundVariable)+ \
        ", LowerBoundVariable: "+str(self.lowerBoundVariable)+", NumberOfTiles: "+str(self.t)+ \
        ", TilesWidth: "+str(self.w)
        
    def get_tiles(self,features):
        """Quantize the features, returns a list containing the value of the tiles for each variable
          The return is a array of arrays, each array consists in the value of a tile for all variables"""
        resultList = []
          
        #Computes the value of each tile    
        for tile in range(0,len(self.tileList)):
          lowLimit = self.tileList[tile][0]
          upperLimit = self.tileList[tile][1]
          
          #Calculates the tile value for all features
          activated = []
          for feature in features:
              test = feature <= upperLimit and feature >= lowLimit
              value = 1 if test==True else 0
              activated.append(value)
          #Include the results for this tile in the return list
          resultList.append(activated)
          
          #Inserted for compactibility
          data = []
          #len(quantVar[0]) is the number of variables
          for i in range(0,len(resultList[0])):
            #Transforms n tuples into a single array
            for var in resultList:
                #copy each tuple value to the output
                data.append(var[i])

        return tuple(data)
              
    
    
    
    def __init__(self, lowerBoundVariables=-1, upperBoundVariables=+1, tilesNumber=10,tileWidth=0.5):
         self.upperBoundVariable = float(upperBoundVariables)
         self.lowerBoundVariable = float(lowerBoundVariables)
         self.t = tilesNumber
         self.w = float(tileWidth)
         
         self.stepTile = (self.upperBoundVariable - self.lowerBoundVariable) / (tilesNumber)
         
         if(math.fabs(tileWidth) < math.fabs(self.stepTile)):
             print ("****Warning - The tileWidth is too low, this tile coding parameterization is prone to be misleading***")
         lastStep = lowerBoundVariables
         #Compute the tiles
         for i in range(0,self.t):
             currentTile = [lastStep,lastStep+self.w]
             self.tileList.append(currentTile)
             lastStep = lastStep+self.stepTile