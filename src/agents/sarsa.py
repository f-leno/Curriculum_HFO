# -*- coding: utf-8 -*-
"""
Created on May 29th, 8:57
SARSA(lambda) simple implementation
@author: Felipe Leno
"""

import random
import math

from .agent import Agent
from .common_features import Agent_Utilities
from .tilemanager import TileManager




class SARSA(Agent):
    
    #Class to control tiles
    tileManager = None
    #Variable for eligibility trace
    stateActionTrace = None
    alpha = None

    
    epsilon = None
    decayRate = None
    
    functions = None
    policy = None
    
    qTable = None
    
    initQ = None #Value to initiate Q-table
    foundState = {}
    

    def __init__(self, seed=12345,alpha=0.2,epsilon=0.1,initQ = 0, decayRate = 0.9):
        
        self.functions = Agent_Utilities()
        self.alpha = alpha
        self.epsilon = epsilon
        self.qTable = {}
        self.stateActionTrace = {}
        self.decayRate = decayRate
        self.initQ = initQ
        self.tileManager = TileManager()
        super(SARSA, self).__init__(seed=seed)
        
        
             
        

            
    
    def select_action(self, state,allowExploration=True):
        """ When this method is called, the agent executes an action based on its Q-table
            The allowExploration can be turned of to select one action without risk of getting
            a random action.
        """
        
        state = self.tileManager.get_tiles(state)
        
        #if state not in self.foundState:
        #    print ("NEW")
        #self.foundState[state] = 1
        
        #If exploring, an exploration strategy is executed
        if self.exploring and allowExploration:
            action =  self.exp_strategy(state)
        #Else the best action is selected
        else:
            #action =  self.exp_strategy(state)
            action = self.policy_check(state)
        
        return action

        
        
    def policy_check(self,state):
        """In case a fixed action is included in the policy cache, that action is returned
        else, the maxQ action is returned"""
        return self.max_Q_action(state,forExploration=False)
        
        
    def max_Q_action(self,state,forExploration):
        """Returns the action that corresponds to the highest Q-value"""
        actions = self.environment.all_actions(forExploration=forExploration)
        if len(actions)==1:
            return actions[0]
        v,a =  self.functions.get_max_Q_value_action(self.qTable,state,actions,self.exploring,self)
        return a
    def get_max_Q_value(self,state,forExploration):
        """Returns the maximum Q value for a state"""
        actions = self.environment.all_actions(forExploration=forExploration)
        if len(actions)==1:
            return self.readQTable(state,actions[0])
        v,a =  self.functions.get_max_Q_value_action(self.qTable,state,actions,self.exploring,self)
        return v
        
        
        
    def exp_strategy(self,state):
        """Returns the result of the exploration strategy"""
        prob = random.random()
        if prob <= self.epsilon:
            allActions = self.environment.all_actions(forExploration=True)
            return random.choice(allActions)
        return self.max_Q_action(state,forExploration=True)
           

    
    def get_Q_size(self):
        """Returns the size of the QTable"""
        return len(self.qTable)
        
    
    def observe_reward(self,state,action,statePrime,reward):
        """Performs the standard Q-Learning Update"""
        if self.exploring:
            state = self.tileManager.get_tiles(state)
            statePrime = self.tileManager.get_tiles(statePrime)
            qValue= self.readQTable(state,action)
            #Checks if a random action was chosen, in this case the stateAction trace
            # is erased (does not make sense anymore)
            #if self.lastChosenAction != action:
            #    self.stateActionTrace = {}
            #Choose the next action without exploration
            self.lastChosenAction = self.select_action(statePrime,allowExploration = False)
            tdError = reward + self.gamma * self.readQTable(statePrime,self.lastChosenAction) - qValue
            #Updates trace
            self.stateActionTrace[(state,action)] = self.stateActionTrace.get((state,action),0) + 1
            #Updates all state-action pairs in the trace
            for stateAction in self.stateActionTrace.keys():
                newQ = self.qTable.get(stateAction,0) + self.alpha * tdError * self.stateActionTrace[stateAction]
                #Decays the trace
                self.stateActionTrace[stateAction] = self.stateActionTrace[stateAction] * self.gamma * self.decayRate
                self.qTable[stateAction] = newQ
        

    def readQTable(self,state,action):             
        """Returns one value from the Qtable"""
        if not (state,action) in self.qTable:
            self.qTable[(state,action)] = self.initQ
        
        return self.qTable[(state,action)] 
        
    def finish_episode(self):
        """Initiates the trace"""
        super(SARSA, self).finish_episode
        self.stateActionTrace = {}
        
        

        


 