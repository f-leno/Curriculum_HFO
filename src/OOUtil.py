#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 14:36:53 

Functions for Object-Oriented proposals
@author: Felipe Leno
"""
from domain.hfostate import HFOStateManager
import copy
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
    if source_task.get_domain_task() == "HFOTask":
        #deals separately with each domain, here with HFO
        for key in quantClass.keys():
            if key=="friend":
                totValue = max(source_task.numberFriends,target_task.numberFriends)
            elif key=='enemy':
                totValue = max(source_task.numberEnemies,target_task.numberEnemies)
            objValue += float(quantClass[key]) / totValue
        #Continuar aqui
        targetStateSpace = target_task.state_space()
        
        intersecStates = 100 * (1-max(source_task.distance,target_task.distance)) * \
              (1+ min(source_task.numberFriends,target_task.numberFriends) + min(source_task.numberEnemies,target_task.numberEnemies))
              
        intersecStates /= targetStateSpace
    else: #Code for the GridWorld Domain
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
        intersecStates /= target_task.state_space()
                            
        
     
    
    
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

def get_PITAM_mappings(state,action,targetTask,previousTasks,previousQTables,getOtherActions=True,allActions=None,agent=None):
    """Defines the PITAM probabilities and qvalues
        state - state for the mapping
        action - action for the mapping
        targetTask: Task to be solved
        previousTasks: previously solved tasks
        previousQTables: Q-tables that can be reused
        getOtherActions: if True, all the possible mappings for the current state will be used, regardless of the
        corresponded action.
    
    """
    if targetTask.get_domain_task() == "HFOTask":
        PITAMMapping = get_PITAM_mappings_hfo(state,action,targetTask,previousTasks,previousQTables,getOtherActions,allActions,agent)
    else:
        PITAMMapping = get_PITAM_mappings_grid(state,action,targetTask,previousTasks,previousQTables,getOtherActions)
    return PITAMMapping

def get_PITAM_mappings_hfo(completeState,action,targetTask,previousTasks,previousQTables,getOtherActions,allActions,agent):
    """PITAM Mapping for the HFO domain"""
    PITAMMappings = []
    #Get the relevant features from the task
    targetFeatures = targetTask.task_features()
    friendsTarget = targetFeatures[0]
    enemiesTarget = targetFeatures[1]
    managerTarget = HFOStateManager(friendsTarget,enemiesTarget)    
    #Sorts the state variables acording to the object-oriented description
    completeState = managerTarget.reorderFeatures(completeState)    
        
    for task in previousTasks:
        if not task.name in previousQTables:
            continue
        qTable = previousQTables[task.name]
        sourceFeatures = task.task_features()                
        friendsSource = sourceFeatures[0]
        enemiesSource = sourceFeatures[1]
        managerSource = HFOStateManager(friendsSource,enemiesSource)
        
        #Information from friend agents
        infoFriend = managerTarget.get_friend_info(completeState)       
        #information from enemies
        infoEnemies = managerTarget.get_enemy_info(completeState)
        #Independent info
        infoIndependent = managerTarget.get_independent_info(completeState)
        
        #Builds combinations of objects as required by PITAM
        combFriends = build_combinations(infoFriend,friendsTarget,friendsSource)
        combEnemies = build_combinations(infoEnemies,enemiesTarget,enemiesSource)
        
        if combFriends == []:
            combFriends = [[]]
        if combEnemies == []:
            combEnemies = [[]]
        
        #Now, build states
        for eleFriend in combFriends:
            for eleEnemies in combEnemies:
                simValue = min(friendsTarget,friendsSource) + min (enemiesTarget,enemiesSource) + 0.1
                #Builds state
                state = managerSource.build_state(eleFriend,eleEnemies,infoIndependent)
                #Prepares for Q-table reuse
                state = managerSource.filter_features(managerSource.reorderFeatures(state))
                state = agent.tileManager.get_tiles(state)
                if getOtherActions:
                    for act in allActions:
                        PITAMMappings.append([(state,act),simValue,qTable.get((state,action),0)])    
                else:
                    PITAMMappings.append([(state,action),simValue,qTable.get((state,action),0)])
        
    #If at least one mapping was found, the relative similarity is calculated
    if len(PITAMMappings) > 0:
         #Get sum of similarity values
         sumSim = sum(list(zip(*PITAMMappings))[1])
           
    #Finishes the similarity calculation
    for pitamTuple in PITAMMappings:
         pitamTuple[1] = pitamTuple[1] / sumSim
         #if pitamTuple[2] != 0:
         #    print("**** FOUND")
    return PITAMMappings

def build_combinations(objects,numberFrom,numberTo):
    """Builds numberTo-combinations of the given set of objects. In case less objects than the desired number are given,
        the objects are repeated"""
    
    returnObjects = []
    if numberFrom < numberTo:
        #If the number of objects is lower than the expected
        # in the destination, the objects are repeated
        returnObjects = copy.deepcopy(objects)
        for i in range(numberTo - numberFrom):
            nextIndex = i % numberFrom
            returnObjects.append(copy.deepcopy(objects[nextIndex]))
        returnObjects = [returnObjects]
    elif numberFrom > numberTo:
        #If the number of objects is higher than the desired destination number,
        # a combination of the objects is processe
        for i in range(numberFrom):
            #get_combinations is a recursive function that will build the combination
            returnObjects.extend(get_combinations(objects, i, numberTo,[]))
    elif numberFrom == numberTo:
        returnObjects.append(copy.deepcopy(objects))

    return returnObjects
            
            
            
def get_combinations(objects,fixedIndex,numberTo,states):
    """A recursive function that at the end will return a list of states."""
    baseState = copy.deepcopy(states)
    #Fix one position in the variable
    if len(baseState)==0:
        baseState.append([copy.deepcopy(objects[fixedIndex])])
    else:
        for state in baseState:
            state.append(copy.deepcopy(objects[fixedIndex]))
            
    currentSize = len(baseState[0])
    #If the desired number of objects was achieved, time to return in the loop
    if currentSize == numberTo:
        return baseState
    
    returnStates = []
    #For all baseStates, one position is fixed and the other ones is defined by the recursive function
    for i in range(fixedIndex+1,len(objects)):
        #If possible, fix another position
        if i + (numberTo - currentSize - 1) < len(objects):
            returnStates.append(get_combinations(objects,i,numberTo,baseState))
            
    #After the recursive function is called multiple times, the states are returned.
    return returnStates
    
    
          
    
def get_PITAM_mappings_grid(state,action,targetTask,previousTasks,previousQTables,getOtherActions):
    """PITAM Mapping for the gridworld domain"""
    setState = set(state)
    PITAMMappings = []
    for task in previousTasks:
          #Get Q-table     
          taskName = task.name
          #In case the pruned curriculum is used and a source task was skipped
          if not taskName in previousQTables:
              continue
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
         sumSim = sum(list(zip(*PITAMMappings))[1])
           
    #Finishes the similarity calculation
    for pitamTuple in PITAMMappings:
         pitamTuple[1] = pitamTuple[1] / sumSim
    return PITAMMappings
    
    