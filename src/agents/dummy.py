# -*- coding: utf-8 -*-
"""
Created on May 26 13:26, 2017
Random agent, no reasoning is performed
@author: Felipe Leno
"""


import random

from .agent import Agent


class Dummy(Agent):

    def __init__(self, seed=12345):
        super(Dummy, self).__init__(seed=seed)
        
    def select_action(self, state):
        """ When this method is called, the agent executes an action. """
        return random.choice(self.environment.all_actions())
    
    def observe_reward(self,state,action,statePrime,reward):
        """ After executing an action, the agent is informed about the state-action-reward-state tuple """
        pass    