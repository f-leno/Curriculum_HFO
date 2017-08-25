#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:42:05 2017

Implementation of the Object-focused Q-Learning
@author: Felipe Leno
"""



import random
import math

from .agent import Agent
from common_features import Agent_Utilities


import domain.actions as actions

class OFQLearning(Agent):
    
    
    
    alpha = None

    
    epsilon = None

    
    functions = None
    policy = None
    
    lastState = None
    
    qTables = None
    
    initQ = None #Value to initiate Q-table

    

    def __init__(self, seed=12345,alpha=0.5,epsilon=0.1,initQ = 0):
        
        self.functions = Agent_Utilities()
        self.alpha = alpha
        self.epsilon = epsilon
        self.qTables = {}
        self.initQ = initQ
        super(OFQLearning, self).__init__(seed=seed)
        
        
             
        

            
    
    def select_action(self, state):
        """ When this method is called, the agent executes an action based on its Q-table """
        self.lastState = self.environment.get_state(True)
        
        #If exploring, an exploration strategy is executed
        if self.exploring:
            action =  self.exp_strategy(state)
        #Else the best action is selected
        else:
            #action =  self.exp_strategy(state)
            action = self.policy_check(state)
        
        return action

        
        
    def policy_check(self,state):
        """The Q-table of each object class is evaluated, and then the action of the maximum value is returned"""
        return self.max_Q_action(state)
        
        
    def max_Q_action(self,state):
        """Returns the action that corresponds to the highest Q-value"""
        actions = self.getPossibleActions()
        
        bestAct = None
        valueBestAct = -float('inf')
        
        #Retunrs action that has the best sum of Q-values for the given state
        for act in actions:
            objects = self.decompose_objects(state)
            
            currentActValue = 0
            
            maxValue = {}
            minValue = {}
            #Count all QValues
            for obj in objects:
                class_obj = obj[0]
                state_obj = obj[1]
                
                if not class_obj in maxValue:
                    maxValue[class_obj] = -float('inf')
                if not class_obj in minValue:
                    minValue[class_obj] = float('inf')
                
                
                #Get Q-table of object class
                qTable = self.select_qTable(class_obj)
                qValue = self.readQObjectTable(state_obj,act,qTable)
                
                
                if maxValue[class_obj] < qValue:
                    maxValue[class_obj] = qValue
                if minValue[class_obj] > qValue:
                    minValue[class_obj] = qValue
                
            #maxValue #+ minValue
            for key in maxValue.keys():
                currentActValue += maxValue[key] + minValue[key]
                
            #Compares if this action is the best so far
            if valueBestAct < currentActValue:
                valueBestAct = currentActValue
                bestAct = [act]
            elif valueBestAct == currentActValue:
                bestAct.append(act)
            
        return random.choice(bestAct)
    def get_max_Q_value(self,state,qTable):
        """Returns the maximum Q value for a state"""
        actions = self.getPossibleActions()
        maxValue = -float('Inf')

        
        for act in actions:
             #print str(type(state))+" - "+str(type(act))
             qV = self.readQObjectTable(state,act,qTable)
             if(qV>maxValue):
                 maxValue = qV
        return maxValue
        
        
        
    def exp_strategy(self,state):
        """Returns the result of the exploration strategy"""
        useBoltz = False        
        allActions = self.getPossibleActions()
        if useBoltz:
            #Boltzmann exploration strategy
            valueActions = []
            sumActions = 0
            
            for action in allActions:
                qValue = self.readQTable(state,action)
                vBoltz = math.pow(math.e,qValue/self.T)
                valueActions.append(vBoltz)
                sumActions += vBoltz
            
            probAct = []
            for index in range(len(allActions)):
                probAct.append(valueActions[index] / sumActions)
            
            rndVal = random.random()
            
            sumProbs = 0
            i=-1
            
            while sumProbs <= rndVal:
                i = i+1
                sumProbs += probAct[i]
            
            return allActions[i]
        else:
            prob = random.random()
            if prob <= self.epsilon:
                return random.choice(allActions)
            return self.max_Q_action(state)
           
       
    
    def observe_reward(self,state,action,statePrime,reward):
        """Performs the standard Q-Learning Update"""
        if self.exploring:
            statePrime = self.environment.get_state(True)
            state = self.lastState
            
            #Object index
            index = 0
            #Perform all Qvalue updates
            for obj in state:
                class_obj = obj[0]
                state_obj = (obj[1],obj[2])
                
                
                #Get reward for current object
                #reward = self.environment.get_obj_reward(class_obj,state_obj)
                #Get Q-table of object class
                qTable = self.select_qTable(class_obj)
                qValue = self.readQObjectTable(state_obj,action,qTable)
                
                #Defines next State of object
                nextState = (statePrime[index][1],statePrime[index][2])
                #Reward related to the object
                reward = self.environment.object_reward(class_obj,nextState)
                #Get V(s' for the current object)
                V = self.get_max_Q_value(nextState,qTable) 
                newQ = qValue + self.alpha * (reward + self.gamma * V - qValue)
                qTable[(state_obj,action)] = newQ
                index += 1

    def readQTable(self,state,action):             
        """Returns one value from the Qtable"""
        objects = self.decompose_objects(state)
        #Sum the Q values for all objects inside the state
        
        qValueState = 0
        for obj in objects:
            class_obj = obj[0]
            state_obj = obj[1]
            #Get Q-table of object class
            qTable = self.select_qTable(class_obj)
            qValueState += self.readQObjectTable(state_obj,action,qTable)
        #Return the sum of QValues for all states
        return qValueState
    
    def readQObjectTable(self,state_obj,action,qTable):
        """Reads the Q-table of a given object, initializating the value if the
        Q-entry does not exist"""
        if not (state_obj,action) in qTable:
            qTable[(state_obj,action)] = self.initQ
        return qTable[(state_obj,action)]
    
    
    def select_qTable(self,objClass):
        """Returns the Qtable belonging to an object class"""
        if not objClass in self.qTables:
            self.qTables[objClass] = {}
        return self.qTables[objClass]
    
    
    def decompose_objects(self,state):
        """Returns a list of objects inside a state in the format (class,state)"""
        objList = []
        
        for obj in state:
            #index 0 = class, index 1 = state (x and y positions)
            objList.append([obj[0],(obj[1],obj[2])])
        
        return objList
        
#        if self.exploring:   
#            qValue= self.readQTable(state,action)
#            V = self.get_max_Q_value(statePrime)        
#            TDError = reward + self.gamma * V - qValue
#            self.stateActionTrace[(state, action)] = self.stateActionTrace.get((state, action), 0) + 1            
#            for stateAction in self.stateActionTrace:
#                # update update ALL Q values and eligibility trace values
#                newQ = qValue + self.alpha * TDError * self.stateActionTrace.get(stateAction, 0)
#                self.qTable[stateAction] = newQ
#                # update eligibility trace Function for state and action
#                self.stateActionTrace[stateAction] = self.gamma * self.decayRate * self.stateActionTrace.get(stateAction, 0)
#            if self.environment.is_terminal_state():
#                    self.stateActionTrace = {} 
#                    self.epsilon = self.epsilon #* self.epsilonDecay

            
            
           
#        if self.exploring:
#            qValue= self.readQTable(state,action)
#            V = self.get_max_Q_value(statePrime)        
#            newQ = qValue + self.alpha * (reward + self.gamma * V - qValue)
#            self.qTable[(state,action)] = newQ
#        
        
    
    def getPossibleActions(self):
        """Returns the possible actions"""
        
        return actions.all_agent_actions()

 