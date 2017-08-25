#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 14:36:53 

Functions for Object-Oriented proposals
@author: Felipe Leno
"""

def task_similarity(source_task,target_task):
    """Calculates task similarity as described in the paper"""
    import copy
    
    stateSource = source_task.init_state()
    stateTarget = target_task.init_state()
    
    stateSource = copy.deepcopy(stateSource)
    stateTarget = copy.deepcopy(stateTarget)
    
    #counts number of intersections per class
    quantClass = {}
    #Find the intersection of objects in those two tasks
    
    for obj in stateSource:
        if not obj[0] in quantClass:
            quantClass[obj[0]] = 0
        if any(obj == objTarget for objTarget in stateTarget):
            stateTarget.remove(obj)
            quantClass[obj[0]] += 1
        
    objValue = 0              
    
    #--------------------------------------------------------------------------
    # This code should be modified to a domain-independent code
    #----------------------------------------------------------------------------
    #After counting the objects, the value for each class is defined
    for key in quantClass.keys():
        if key=='treasure':
            totValue = max(source_task.num_treasures(),target_task.num_treasures())
        elif key=='fire':
            totValue = max(source_task.num_fires(),target_task.num_fires())
        elif key=='pit':
            totValue = max(source_task.num_pits(),target_task.num_pits())
        elif key=='agent':
            totValue = 1
        objValue += float(quantClass[key]) / totValue
                        
        
     
    #intersection of states
    intersecStates = float(min(source_task.get_sizeX(),target_task.get_sizeX()) * min(source_task.get_sizeY(),target_task.get_sizeY()))
    intersecStates /= target_task.get_sizeX()*target_task.get_sizeY()
    
    #--------------------------------------------------------------------------
    # End of code to be changed
    #----------------------------------------------------------------------------
    
                         
    similarity = objValue + intersecStates
    #Using previous equation
    #Values related to the grid size (degrees of freedom)
    #difSizeX = 1 if source_task.get_sizeX() == target_task.get_sizeX() else 0
    #difSizeY = 1 if source_task.get_sizeY() == target_task.get_sizeY() else 0
    
    #similarity = objValue + difSizeX + difSizeY
    return similarity
        
def total_num_obj(task):
    """Returns the number of objects for a given task"""
    return len(task.init_state()) + 1 #num of objects + agent

def get_PITAM_mappings(state,action,previousTasks,previousQTables,getOtherActions=True):
    """Defines the PITAM probabilities and qvalues
        state - state for the mapping
        action - action for the mapping
        previousTasks: previously solved tasks
        previousQTables: Q-tables that can be reused
        getOtherActions: if True, all the possible mappings for the current state will be used, regardless of the
        corresponded action.
    
    """
    setState = set(state)
    PITAMMappings = []
    for task in previousTasks:
          #Get Q-table     
          taskName = task.name
          qTable = previousQTables[taskName]
                
          for stateAction in qTable.keys():
              #Should other actions be taken into account for this state?
              if getOtherActions or stateAction[1]==action:
                    #Get state from tuple
                    stateSimple = set(stateAction[0])
                    #Is the set of states contained?
                    if setState.issuperset(stateSimple) or setState.issubset(stateSimple):
                        #The number of common objects is the smaller number of objects
                        numComObj = min(len(stateSimple),len(setState)) 
                        #Get the state-action pair, similarity, and q-value
                        PITAMMappings.append([stateAction,numComObj,qTable[stateAction]])
                        
                
    #If at least one mapping was found, the relative similarity is calculated
    if len(PITAMMappings) > 0:
         #Get sum of similarity values
         sumSim = sum(zip(*PITAMMappings)[1])
           
    #Finishes the similarity calculation
    for pitamTuple in PITAMMappings:
         pitamTuple[1] = pitamTuple[1] / sumSim
    return PITAMMappings
    