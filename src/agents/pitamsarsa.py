#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 07:30:30 2017
Implementation of PITAM knowledge reuse using SARSA
@author: Felipe Leno
"""


from agents.sarsa import SARSA
from domain.hfostate import HFOStateManager
import OOUtil

class PITAMSARSA(SARSA):

    nextAction = None
    currentTask = None
    
    previousTasks = None  #Tasks to reuse the Q-table
    
    previousQTables = {}
    
    calculatedPITAM = {}
    useBias = False
    
    calcAverage = True #If true, the average value is transferred, if false, the maximum is transferred.
    
    savedPot = {}
    
    def __init__(self,seed=12345,alpha=0.7,epsilon=0.1,initQ = 0, decayRate = 0.92):#alpha=0.7,epsilon=0.1,initQ = 0, decayRate = 0.92):Given
        
        super(PITAMSARSA, self).__init__(seed=seed,alpha=alpha,epsilon=epsilon,initQ=initQ,decayRate=decayRate)
        
 
    
    def readQTable(self,state,action):             
        """Returns one value from the Qtable"""
        if not (state,action) in self.qTable:
            self.init_Q(state,action)
        return self.qTable[(state,action)] 
            
    def set_current_task(self,task):
        super(PITAMSARSA, self).set_current_task(task)
        self.previousTasks = self.curriculum.previous_tasks(task)
        
    def init_Q(self,state,action):
        """ Initiates a new entry in the Q-table using the PITAM algorithm"""
        if len(self.previousTasks)==0:
            self.qTable[(state,action)] = self.initQ
            return
        
        #If the agent has calculated PITAM before for the current state this value is reused.
        #Else, a new value is calculated
        if state in self.calculatedPITAM:
            PITAMMappings = self.calculatedPITAM[state]
        else:        
            actions = self.environment.all_actions()
            if self.currentTask.get_domain_task() == "HFOTask":
                #completeState = self.environment.hfoObj[self.agentIndex].getState()
                completeState = self.environment.hfoObj.getState()
                PITAMMappings = OOUtil.get_PITAM_mappings(completeState,action,self.currentTask,self.previousTasks,self.previousQTables,getOtherActions=self.useBias,allActions=actions,agent=self)
            else:
                PITAMMappings = OOUtil.get_PITAM_mappings(state,action,self.currentTask,self.previousTasks,self.previousQTables,getOtherActions=self.useBias,allActions=actions,agent=self)
            #First define the PITAM, then initiate the Q-table
            
                         
            #Stores for later use
            self.calculatedPITAM[state] = PITAMMappings
        
        #Defines the initialization method and calls it
        if self.useBias:
            self.init_with_bias(state,action,PITAMMappings)
        else:
            self.init_with_average(state,action,PITAMMappings)
                    
                
    def init_with_bias(self,state,action,PITAMMappings):
        """introduces a bias in the best action according to PITAM mapping"""
        valueActions = {} #Value for each action
        
        if PITAMMappings == []:
            self.qTable[(state,action)] = self.initQ
            return
        
        #calculates the weighted value for each action
        for pitamTuple in PITAMMappings:
            
            #QValue * PITAM probability
            valueAct = pitamTuple[2] * pitamTuple[1] 
            actTuple = pitamTuple[0][1]
            
            if not actTuple in valueActions:
                valueActions[actTuple] = 0
            valueActions[actTuple] += valueAct        
        
        #defines the best action (highest value)
        bestAction = max(valueActions, key=lambda i: valueActions[i])
        
        #initiate all found actions in the QTable, only the best one with bias
        for act in valueActions.keys():
            if act==bestAction:
                self.qTable[(state,act)] = self.biasValue
            else:
                self.qTable[(state,act)] = self.initQ
                
                
                
        
    def init_with_average(self,state,action,PITAMMappings):
        """Calculates the weighted average taking into account the PITAM probabilities"""
        if self.calcAverage:
            sumQs = 0
        else:
            sumQs = -float('inf')
            
        if PITAMMappings == []:
            self.qTable[(state,action)] = 0
            return
        numFound = 0
        for pitamTuple in PITAMMappings:
            #QValue * PITAM probability
            newValue = pitamTuple[2] * pitamTuple[1] 
               
            if self.calcAverage:
                sumQs += newValue
                numFound += 1
            elif newValue > sumQs:
                sumQs = newValue
                    
        if self.calcAverage and numFound > 0:           
            sumQs = float(sumQs) / numFound
            
        self.qTable[(state,action)] = sumQs
                    
           

    def finish_learning(self):
        """End of one task"""
        self.store_q_table()
        self.qTable = {}
        self.calculatedPITAM = {}
        
    def store_q_table(self):
        """ssociate the current QTable to the current task, as preparation to 
        forget the  q-table"""
        self.previousQTables[self.currentTask.name] = self.qTable

