#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 08:50:15 2017
Agent that learns using PITAM for reward Shaping
@author: Felipe Leno
"""


from agents.rewardshapingqlearning import RewardShapingQLearning
import OOUtil
class PITAMRSQLearning(RewardShapingQLearning):

    calculatedPITAM = {}

    def phi(self,state,action):
        """Calculates the contribution of previous tasks using PITAM"""
        
        #The potential is only computed once
        if (state,action) in self.savedPot:
            return self.savedPot[(state,action)]
        
        phiValue = 0


        
        #If the agent has calculated PITAM before for the current state this value is reused.
        #Else, a new value is calculated
        if state in self.calculatedPITAM:
            PITAMMappings = self.calculatedPITAM[state]
        else:        
            #First define the PITAM, then calculates the contribution from previous Q-tables
            PITAMMappings = OOUtil.get_PITAM_mappings(state,action,self.previousTasks,self.previousQTables,getOtherActions=False)
                         
            #Stores for later use
            self.calculatedPITAM[state] = PITAMMappings
        
        #Defines the initialization method and calls it
        if PITAMMappings != []:
            phiValue = self.get_PITAM_averages(action,PITAMMappings)
        
        
        
        self.savedPot[(state,action)] = phiValue
        return phiValue
            
 
    def get_PITAM_averages(self,action,PITAMMappings):
        """Calculates the potential function based on the PITAM Mapping"""
        sumQs = 0
                
        for pitamTuple in PITAMMappings:
            #Check if the action is the same
            if pitamTuple[0][1] == action:
                #QValue * PITAM probability
                sumQs += pitamTuple[2] * pitamTuple[1] 
        return sumQs
    
    def finish_learning(self):
        """End of one task"""
        self.calculatedPITAM = {}
        super(PITAMRSQLearning,self).finish_learning()

