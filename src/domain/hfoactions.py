#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 14:40:52 2017
Interface for HFO actions
@author: Felipe Leno
"""
import hfo
passInterfaceInit = 20


def is_pass_action(action):
    """Verifies if a given action is a PASS action. In practice, this can be 
        verified comparing the passInterfaceInit attribute with the action 
        number"""
    return action >= passInterfaceInit

def pass_index(action):
    """Returns the index of the agent to pass the ball. As smaller the action
    index, as smaller the distance between the agents"""
    return action - passInterfaceInit

def all_actions(numberFriends, withBall, forExploration=False):
    """Returns all the possible actions for the current situation. If more than
    one PASS action is available, the SHOOT and DRIBBLE actions will be returned
    multiple times"""
    
    if forExploration:
        actions = []
    else:
        #In case the agent is not exploring, those actions are added here because
        #they won't be added later
        actions = [hfo.SHOOT,hfo.DRIBBLE]
    #If the agent gas the ball, more actions are available
    if withBall:
    
        if numberFriends > 0:
            i = 0
            #Creates a Pass action to each friend agent
            while i<numberFriends:
                #Includes SHOOT and DRIBBLE multiple times to avoid making agents
                #pass the ball too often in the random action selection
                if forExploration:
                    actions.append(hfo.SHOOT)
                    actions.append(hfo.DRIBBLE)
                actions.append(passInterfaceInit + i) #Pass action
                i += 1
                
        else:
            actions = [hfo.SHOOT,hfo.DRIBBLE]
    else:
        actions = [hfo.MOVE]
        
    return actions