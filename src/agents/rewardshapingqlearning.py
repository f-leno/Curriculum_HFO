#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 15:03:19 2017
 QLearning using the Curriculum learning approach proposed by Svetlik et al.
 
@author: Felipe Leno
"""
from agents.qlearning import QLearning

class RewardShapingQLearning(QLearning):

    nextAction = None
    currentTask = None
    
    previousTasks = None  #Tasks to reuse the Q-table
    
    previousQTables = {}
    
    savedPot = {}
    
    def __init__(self, seed=12345,alpha=0.5,epsilon=0.1,initQ=0):
        
        super(RewardShapingQLearning, self).__init__(seed=seed,alpha=alpha,epsilon=epsilon,initQ=initQ)
        
    def select_action(self, state):
        """ When this method is called, the agent executes an action based on its Q-table """
        #If the next action was already processed by the reward shaping, this one is returned
        if self.nextAction != None:
            return self.nextAction
        
        return super(RewardShapingQLearning, self).select_action(state)
    
    def observe_reward(self,state,action,statePrime,reward):
        """Performs the standard Q-Learning Update"""
        #shape reward and then use the regular Q-Learning update
        if self.exploring:
            reward = self.shape_reward(state,action,statePrime,reward)
        super(RewardShapingQLearning, self).observe_reward(state,action,statePrime,reward)
        
    def shape_reward(self,state,action,statePrime,reward):
        """Processes the potential function as described in the paper"""
        #Updates the next action
        self.nexAction = None
        self.nexAction = self.select_action(statePrime)
        
        f = self.gamma * self.phi(statePrime,self.nexAction) - self.phi(state,action)
        
        reward = reward + f
        return reward
    def phi(self,state,action):
        """Calculates the contribution of previous tasks"""
        
        #The potential is only computed once
        if (state,action) in self.savedPot:
            return self.savedPot[(state,action)]
        
        phiValue = 0
        #Sum of Q-tables of all previous tasks.
        for task in self.previousTasks:
            taskName = task.name
            qTable = self.previousQTables[taskName]
            averageQ = self.find_average_Q(qTable,state,action)
            phiValue += averageQ
        
        self.savedPot[(state,action)] = phiValue
        return phiValue
            
    def set_current_task(self,task):
        super(RewardShapingQLearning, self).set_current_task(task)

        self.previousTasks = self.curriculum.previous_tasks(task)
    def find_average_Q(self,qTable,state,action):
        """ search inside Q table for all states that fit inside the current Q"""
        setState = set(state)
        sumQ = 0
        numFound = 0
        for stateAction in qTable.keys():
            #same action?
            if stateAction[1] == action:
                stateSimple = set(stateAction[0])
                #Is the set of states contained?
                if setState.issuperset(stateSimple) or setState.issubset(stateSimple):
                    sumQ += qTable[(stateAction)]
                    numFound += 1
        if numFound > 0:
            #if self.currentTask.name=="target":
            #    print str(state) + " "+str(sumQ/numFound)
            return sumQ / numFound
        return 0
                    
                
        
    def finish_episode(self):
        """ Informs the agent about the end of an episode """""
        self.nextAction = None
    def finish_learning(self):
        """End of one task"""
        self.store_q_table()
        self.currentTask = None
        self.savedPot = {}
        self.qTable = {}
        
    def store_q_table(self):
        """ssociate the current QTable to the current task, as preparation to 
        forget the  q-table"""
        self.previousQTables[self.currentTask.name] = self.qTable
