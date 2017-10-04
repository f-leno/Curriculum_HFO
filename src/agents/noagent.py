#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 08:59:39 2017
Empty class to skip agent interactions
@author: leno
"""

# -*- coding: utf-8 -*-
"""
Created on May 29th, 8:57
SARSA(lambda) simple implementation
@author: Felipe Leno
"""

import random


from .agent import Agent
from .common_features import Agent_Utilities
from .tilemanager import TileManager




class NoAgent(Agent):
    
  
    

    
        
             
        

            
    
    def select_action(self, state,allowExploration=True):
        """ When this method is called, the agent executes an action based on its Q-table
            The allowExploration can be turned of to select one action without risk of getting
            a random action.
        """
        actions = self.environment.all_actions(forExploration=allowExploration)
        #Returns any action
        return actions[0]

        
     
    def get_Q_size(self):
        """Returns the size of the QTable"""
        return len(self.qTable)
        
    
    def observe_reward(self,state,action,statePrime,reward):
        """Performs the standard Q-Learning Update"""
        pass
        

 
        
    def finish_episode(self):
        """Initiates the trace"""
        pass
        
        

        


 