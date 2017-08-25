#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 08:48:16 2017
 Using transfer of Value Functions
@author: Felipe Leno
"""

from agents.qlearning import QLearning

class VFReuseQLearning(QLearning):

    nextAction = None
    currentTask = None
    
    previousTasks = None  #Tasks to reuse the Q-table
    
    previousQTables = {}
    
    calcAverage = None #If true, the average value is transferred, if false, the maximum is transferred.
    
    savedPot = {}
    
    def __init__(self, seed=12345,alpha=0.5,epsilon=0.1,initQ=0,calcAverage=True):
        
        super(VFReuseQLearning, self).__init__(seed=seed,alpha=alpha,epsilon=epsilon,initQ=initQ)
        
 
    
    def readQTable(self,state,action):             
        """Returns one value from the Qtable"""
        if not (state,action) in self.qTable:
            self.qTable[(state,action)] = self.find_average_Q(state,action)
        return self.qTable[(state,action)] 
            
    def set_current_task(self,task):
        super(VFReuseQLearning, self).set_current_task(task)
        self.previousTasks = self.curriculum.previous_tasks(task)
        
    def find_average_Q(self,state,action):
        """ search inside Q table for all states that fit inside the current Q"""
        setState = set(state)
        sumQ = 0
        nTasks = 0
        
        
        for task in self.previousTasks:
            numFound = 0
            taskName = task.name
            qTable = self.previousQTables[taskName]
            if self.calcAverage:
                qTask = 0
            else:
                qTask = -float('inf')
            
            for stateAction in qTable.keys():
                #same action?
                if stateAction[1] == action:
                    stateSimple = set(stateAction[0])
                    #Is the set of states contained?
                    if setState.issuperset(stateSimple) or setState.issubset(stateSimple):
                        #Should the average of all possible states be calculated?
                        if self.calcAverage:
                            qTask += qTable[(stateAction)]
                        elif qTask < qTable[(stateAction)]:
                            qTask = qTable[(stateAction)]
                            
                        numFound += 1
            if numFound > 0:
                nTasks += 1
                #If the average should be calculated, more than one qValue is in qTask
                if self.calcAverage:
                    sumQ += qTask / numFound
                else:
                    sumQ += qTask  
                
        if nTasks > 0:
            #if self.currentTask.name=="target":
            #    print str(state) + " "+str(sumQ/numFound)
            return sumQ / nTasks
        return self.initQ
                    
                
        

    def finish_learning(self):
        """End of one task"""
        self.store_q_table()
        self.qTable = {}
        
    def store_q_table(self):
        """ssociate the current QTable to the current task, as preparation to 
        forget the  q-table"""
        self.previousQTables[self.currentTask.name] = self.qTable
