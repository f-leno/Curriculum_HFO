#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 14:18:58 2017

Class to store all task parameters (can be built from text files)

@author: Felipe Leno
"""
from domain.task import Task
class GridWorldTask(Task):
    
    #Task Parameters and initial state
    sizeX     = None
    sizeY     = None
    pits      = None
    fires     = None
    treasures = None
    initState = None
    
    #Relevant classes for transfer potential computation
    relevantClasses = ["fire",'pit']

    
    taskString = None
    
    def __init__(self, filePath=None,taskName="noName",taskData=None):
        """ The source file must be a text file specified as follows:
            <sizeX>;<sizeY>;<objects>
            where <objects> is any number of objects separated with commas and obeying the format:
            <type>:<xPosic>-<yPosic>,<type>:<xPosic>-<yPosic>
            
        """
        super(GridWorldTask, self).__init__(filePath,taskName,taskData)
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
            
        self.sizeX = int(sep[0])
        self.sizeY = int(sep[1])
        
        self.initState = self.load_task_state(sep[2])
        
        #Used for recovering the initial state
        self.taskString = sep[2]
        
        #Extracts the number of objects of each type.
        self.treasures = sep[2].count('treasure')
        self.pits = sep[2].count('pit')
        self.fires = sep[2].count('fire')
        
    def num_pits(self):
        return self.pits
    def task_features(self):
        return (self.fires,self.pits)
        
    def num_fires(self):
        return self.fires
        
    def get_sizeX(self):
        return self.sizeX
        
    def get_sizeY(self):
        return self.sizeY
        
    def num_treasures(self):
        return self.treasures
    def init_state(self):
        return self.initState
       
   
    def __hash__(self):
        """Returns a hash for the task"""
        #taskTuple = tuple([self.sizeX,self.sizeY,tuple(self.initState)])
        taskTuple = tuple([self.sizeX,self.sizeY,self.name])
        return hash(taskTuple)
    

    
    def load_task_state(self,taskState):
        """Load a textual description of the state to an internal state
            Objects are separated by commas, in the format <type>:<xPosic>-<yPosic>
            type can be: 'agent', 'treasure',pit, or fire
        """
        objects = taskState.split(',')
        
        taskInfo = []
        for obj in objects:
            clasSpt = obj.split(":")
            posics = clasSpt[1].split('-') 
            taskInfo.append([clasSpt[0],int(posics[0]),int(posics[1])])
            
        import operator
        taskInfo.sort(key=operator.itemgetter(0, 1, 2))
    
        return taskInfo
        
    def transfer_potential(self,targetTask):
        """Calculates the transfer potential between two tasks"""
        sourceTask = self
        sizeXSource = sourceTask.get_sizeX()
        sizeYSource = sourceTask.get_sizeY()
        
        sizeXTarget = targetTask.get_sizeX()
        sizeYTarget = targetTask.get_sizeY()
        
        locationTraceSource = []
        locationTraceTarget = []
        #For all possible position, calculates the distance between the objects
        for x in range(1,sizeXSource+1):
            for y in range(1,sizeYSource+1):
                distances = []
                #Iterates over all objects in the source task
                for obj in sourceTask.init_state():
                    #If it is an obstacle, stores the distance
                    if obj[0] in sourceTask.relevantClasses :
                        distances.append([(x - obj[1],y - obj[2],obj[0])]) 
                #Stores distances for that position
                locationTraceSource.append(distances)
        #Now, the same thing is done for the targetTask
        
        for x in range(1,sizeXTarget+1):
            for y in range(1,sizeYTarget+1):
                distances = []
                #Iterates over all objects in the source task
                for obj in targetTask.init_state():
                    #If it is an obstacle, stores the distance
                    if obj[0] in targetTask.relevantClasses :
                        distances.append([(x - obj[1],y - obj[2],obj[0])]) 
                #Stores distances for that position
                locationTraceTarget.append(distances)
        
        applicable = 0
        for distSource in locationTraceSource:
            for distTarget in locationTraceTarget:
                #If equivalent state exists
                if all(x in distTarget for x in distSource):
                    applicable += 1
                    
        #Now, calculates potential
        pot = float(applicable) / (1 + sizeXTarget*sizeYTarget - sizeXSource*sizeYSource)
        return pot
        
        
    
    def state_space(self):
        """Returns the state space of this task"""
        return self.get_sizeX() * self.get_sizeY() 
        sizeStateSpaceTarget = target_task.get_sizeX() * target_task.get_sizeY()
        

    def number_objects(self):
        """Returns the number of objects if the object-oriented description is used."""
        return self.num_pits() + self.num_fires()

