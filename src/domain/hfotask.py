#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 10:02:12 2017
Task object for the HFO domain
@author: Felipe Leno
"""
#from domain.task import Task
from domain.task import Task
import random
class HFOTask(Task):
    numberFriends   = None
    numberEnemies   = None
    strategy        = None
    distance        = None
    seed            = None
    
    
    def __init__(self, filePath=None,taskName="noName",taskData=None):
        """ The source file must be a text file specified as follows:
                <number_of_friends>;<number_of_enemies>;<strategy>;<distance>;<seed>
                <number_of_friends> - from 0 to 4, number of teammates
                <number_of_enemies> - from 0 to 5, number of opponents
                <strategy> - opponents' strategy. 'base' or 'helios'
                <distance> - distance to goal 0.1 - 0.9 
                <seed> - seed for allowing repetition, 0=random
                <onlyNpc> - If true, only npcs are executed, no learning agent
        """
        super(HFOTask, self).__init__(filePath,taskName,taskData)
        self.name = taskName
        #Read task file
        if filePath != None:
            with open(filePath, 'r') as content_file:
                content = content_file.read()
        else:
            #Read task data
            content = taskData
            
        #get size the grid size
        sep = content.split(';')
            
        self.numberFriends = int(sep[0])
        self.numberEnemies = int(sep[1])
        self.strategy = sep[2]
        self.distance = float(sep[3])
        self.seed = int(sep[4])
        
        #Specifying 0 of seed means random seed
        if self.seed==0:
            self.seed = random.randint(1,10000)
        
    def task_features(self):
        return tuple([self.numberFriends,self.numberEnemies,self.strategy,self.distance,self.seed])
        
       
   
    def __hash__(self):
        """Returns a hash for the task"""
        #taskTuple = tuple([self.sizeX,self.sizeY,tuple(self.initState)])
        taskTuple = tuple([self.numberFriends,self.numberEnemies,self.strategy,self.distance,self.name])
        return hash(taskTuple)
    

    
    def transfer_potential(self,targetTask):
        """Calculates the transfer potential between two tasks
           The state space is here estimated as if each of the state variables could
           assume 10 values. This is not true because most of the state variables are
           continuous, however, this calculation is fast and 
        
        """
        sourceTask = self
        stateSpaceSource = 100 * (1-sourceTask.distance) * (1+ sourceTask.numberFriends + sourceTask.numberEnemies)
        stateSpaceTarget = 100 * (1-targetTask.distance) * (1+ targetTask.numberFriends + targetTask.numberEnemies)
        
        qInCommon = 100 * \
                    min(1-sourceTask.distance, 1-targetTask.distance) * \
                    (1 + min(sourceTask.numberFriends,targetTask.numberFriends) + min(sourceTask.numberEnemies,targetTask.numberEnemies))
                    
        transferPot = qInCommon / (1 + stateSpaceTarget - stateSpaceSource)
        return transferPot
    
    
def is_contained(featuresSource,featuresTarget):
    """Returns if the features of the target task contains all features from the
    source task (only the number of friends and enemies matter)"""
    
    #Number friends and number enemies matter
    return featuresSource[0] <= featuresTarget[0] and featuresSource[1] <= featuresTarget[1] 