#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 15:38:57 2017
 Abstract Class for Task Classes
@author: Felipe Leno
"""
import abc

class Task(object):
    """Abstract class describing a task"""
    name      = None
    
    @abc.abstractmethod      
    def init_state(self):
        pass
    @abc.abstractmethod      
    def load_task_state(self,taskState):
        """Loads a textual description of the state to an internal state
            Objects are separated by commas, in the format <type>:<xPosic>-<yPosic>
            type can be: 'agent', 'treasure',pit, or fire for the gridworlddomain
        """
        pass
    def __str__(self):
        return self.name  
    
    def __init__(self, filePath=None,taskName="noName",taskData=None):
        self.name = taskName
        
        
        
        
        
    @abc.abstractmethod       
    def transfer_potential(self,targetTask):
        """Calculates the transfer potential between two tasks"""
        pass
    
    
def is_contained(featuresSource,featuresTarget):
    """Returns if the features of the target task contains all features from the
    source task"""
    return featuresSource[0] <= featuresTarget[0] and featuresSource[1] <= featuresTarget[1] 