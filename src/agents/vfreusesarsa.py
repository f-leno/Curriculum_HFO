#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 15:03:28 2017
Value Function reuse
@author: Felipe Leno
"""


from agents.sarsa import SARSA
from domain.hfostate import HFOStateManager

class VFReuseSARSA(SARSA):

    nextAction = None
    currentTask = None
    
    previousTasks = None  #Tasks to reuse the Q-table
    
    previousQTables = {}
    
    calcAverage = None #If true, the average value is transferred, if false, the maximum is transferred.
    
    savedPot = {}
    
    def __init__(self,seed=12345,alpha=0.7,epsilon=0.1,initQ = 0, decayRate = 0.92):
        
        super(VFReuseSARSA, self).__init__(seed=seed,alpha=alpha,epsilon=epsilon,initQ=initQ,decayRate=decayRate)
        
 
    
    def readQTable(self,state,action):             
        """Returns one value from the Qtable"""
        if not (state,action) in self.qTable:
            self.qTable[(state,action)] = self.find_average_Q(state,action)
        return self.qTable[(state,action)] 
            
    def set_current_task(self,task):
        super(VFReuseSARSA, self).set_current_task(task)
        self.previousTasks = self.curriculum.previous_tasks(task)
        
    def find_average_Q(self,state,action):
        """ search inside Q table for all states that fit inside the current Q"""
       
        numFound = 0
        if self.calcAverage:
            finalQ = 0
        else:
            finalQ = -float('inf')
        #Sums the qValue (or get the maximum) from all possible previous tasks and average it
        for task in self.previousTasks:
            
            taskName = task.name
            qTable = self.previousQTables[taskName]
            #Translates the current state and get the Q value
            qTask,found = self.recoverTranslatedQ(qTable,self.environment.hfoObj.getState(),action,task,self.currentTask)
            
            #Updates the Q value
            if self.calcAverage:
                finalQ += qTask
                if found:
                    numFound += 1
            else:
                if qTask > finalQ:
                    finalQ = qTask
            
        #calculates the average if applicable
        if numFound > 0:
                if self.calcAverage:
                    finalQ = finalQ / numFound
                
                return finalQ

        return self.initQ
                    
                
    def recoverTranslatedQ(self,sourceQTable,currentCompleteState,currentAction,sourceTask,currentTask):
        """Translates the state between HFO tasks. when more agents exist in one of the tasks, the closes one
           is taken. This same strategy is valid for both friends or enemies
           The return are the Qvalue extrated from the source task, and a boolean indicating if any transfer was possible
        """
        sourceFeatures = sourceTask.task_features()
        currentFeatures = currentTask.task_features()
           
        friendsSource = sourceFeatures[0]
        enemiesSource = sourceFeatures[1]
        friendsCurrent = currentFeatures[0]
        enemiesCurrent = currentFeatures[1]
        
        managerSource = HFOStateManager(friendsSource,enemiesSource)
        managerTarget = HFOStateManager(friendsCurrent,enemiesCurrent)
        
        currentCompleteState = managerTarget.reorderFeatures(currentCompleteState)
        
        #Information from friend agents
        infoFriend = managerTarget.get_friend_info(currentCompleteState)
        if friendsSource > friendsCurrent:
            #In case the source task has more friends, we repeat the farther objects
            for i in range(1,friendsSource - friendsCurrent + 1):
                infoFriend.append(infoFriend[len(infoFriend)-i])
        elif friendsSource < friendsCurrent:
            #If the target task has less friends, then only the closest ones are considered
            infoFriend = infoFriend[0:friendsSource]
        
        #The same procedure is executed for enemies
        infoEnemies = managerTarget.get_enemy_info(currentCompleteState)
        if enemiesSource > enemiesCurrent:
            #In case the source task has more friends, we repeat the farther objects
            for i in range(1,enemiesSource - enemiesCurrent + 1):
                infoEnemies.append(infoEnemies[len(infoEnemies)-i])
        elif enemiesSource < enemiesCurrent:
            #If the target task has less friends, then only the closest ones are considered
            infoEnemies = infoEnemies[0:enemiesSource]
        #Other info are simply copied
        infoIndependent = managerTarget.get_independent_info(currentCompleteState)    
        
        state = managerSource.build_state(infoFriend,infoEnemies,infoIndependent)
        state = managerSource.filter_features(managerSource.reorderFeatures(state))
        #The approximation function is then used
        state = self.tileManager.get_tiles(state)
         
        #Then, recoveries the translated state from the Qtable if possible.
        qValue = 0
        found = (state,currentAction) in sourceQTable
        if found:
            #print("FOUND --- "+str(sourceQTable[(state,currentAction)]))
            qValue = sourceQTable[(state,currentAction)]
        return qValue,found
           

    def finish_learning(self):
        """End of one task"""
        self.store_q_table()
        self.qTable = {}
        
    def store_q_table(self):
        """ssociate the current QTable to the current task, as preparation to 
        forget the  q-table"""
        self.previousQTables[self.currentTask.name] = self.qTable

