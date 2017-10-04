#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 16:00:06 2017
Code to make it easier to deal with the state space in HFO
@author: Felipe Leno
"""
import numpy as np
import math
class HFOStateManager(object):
    """Performs all needed transformations in the state space"""
    #Number of friends and opponents in the task
    numberFriends = None
    numberOpponents = None
    
    def __init__(self,numberFriends,numberOpponents):
        """The constructor takes as arguments the number of friends and opponents,
        compiling the index of each state variable"""
        self.numberFriends = numberFriends
        self.numberOpponents = numberOpponents
        self.compile_variables()
    
    def filter_features(self,stateFeatures):
        """Filters the HFO features returning only the relevant features"""
        #Maybe it is a good idea to sort opponents/friends
        #Removed Features
        remove = [self.X_POSITION,
                  self.Y_POSITION,
                  self.ORIENTATION,
                  self.BALL_X,
                  self.BALL_Y,
                  self.ABLE_KICK,
                  #self.CENTER_PROXIMITY,
                  #self.GOAL_ANGLE,
                  #self.GOAL_OPENING,
                  #self.OPPONENT_PROXIMITY,
                  #self.FRIEND1_GOAL_OPENING,self.FRIEND2_GOAL_OPENING,self.FRIEND3_GOAL_OPENING,self.FRIEND4_GOAL_OPENING,
                  self.FRIEND1_OPP_PROXIMITY,self.FRIEND2_OPP_PROXIMITY,self.FRIEND3_OPP_PROXIMITY,self.FRIEND4_OPP_PROXIMITY,
                  self.FRIEND1_PASS_OPENING,self.FRIEND2_PASS_OPENING,self.FRIEND3_PASS_OPENING,self.FRIEND4_PASS_OPENING,
                  self.FRIEND1_X,self.FRIEND2_X,self.FRIEND3_X,self.FRIEND4_X,
                  self.FRIEND1_Y,self.FRIEND2_Y,self.FRIEND3_Y,self.FRIEND4_Y,
                  self.FRIEND1_NUMBER,self.FRIEND2_NUMBER,self.FRIEND3_NUMBER,self.FRIEND4_NUMBER,
                  self.OPP1_X,self.OPP2_X,self.OPP3_X,self.OPP4_X,self.OPP5_X,
                  self.OPP1_Y,self.OPP2_Y,self.OPP3_Y,self.OPP4_Y,self.OPP5_Y,
                  self.OPP1_NUMBER,self.OPP2_NUMBER,self.OPP3_NUMBER,self.OPP4_NUMBER,self.OPP5_NUMBER,
                  self.LAST_ACTION_SUCESS,
                 ]
        #Sorts friends by distance
        self.reorderFeatures(stateFeatures)
        
        #Remove from the list attributes that do not exist
        remove = [x for x in remove if x is not None]
        stateFeatures = np.delete(stateFeatures,remove)
        


        return tuple(stateFeatures.tolist())
    
    def reorderFeatures(self,stateFeatures):
        """
            Calculates the distance between the agent and each friendly unit
            and then sorts the attributes according to the distance
            (for example, FRIEND1_Y corresponds to the closest friend)
            This is needed because of the PASS actions, which take into account
            the distance of friendly agents
        """
        
        #if there is at least two friends
        if self.FRIEND2_X != None:
                #Sort Friends by euclidian distance
                listProx = [math.hypot(stateFeatures[self.FRIEND1_X]- stateFeatures[self.X_POSITION], 
                                   stateFeatures[self.FRIEND1_Y]- stateFeatures[self.Y_POSITION])]
                listProx.append(math.hypot(stateFeatures[self.FRIEND2_X]- stateFeatures[self.X_POSITION], 
                                   stateFeatures[self.FRIEND2_Y]- stateFeatures[self.Y_POSITION]))
                
                
                if self.FRIEND3_X != None:
                    listProx.append(math.hypot(stateFeatures[self.FRIEND3_X]- stateFeatures[self.X_POSITION], 
                                   stateFeatures[self.FRIEND3_Y]- stateFeatures[self.Y_POSITION]))
                    
                    if self.FRIEND4_X != None:
                        listProx.append(math.hypot(stateFeatures[self.FRIEND4_X]- stateFeatures[self.X_POSITION], 
                                   stateFeatures[self.FRIEND4_Y]- stateFeatures[self.Y_POSITION]))
                        
            
                #Get list of friends' indexes in descending order according to proximity
                idsOrder = sorted(range(len(listProx)), key=lambda k: listProx[k])
                
                #Get the sorted list and prepares the values to be changed
                copyList = []
                for i in range(len(listProx)):
                    #Values from one of the friends
                    copyList.append([
                            stateFeatures[getattr(self, 'FRIEND'+str(idsOrder[i]+1)+'_GOAL_OPENING')],
                            stateFeatures[getattr(self, 'FRIEND'+str(idsOrder[i]+1)+'_OPP_PROXIMITY')],
                            stateFeatures[getattr(self, 'FRIEND'+str(idsOrder[i]+1)+'_PASS_OPENING')],
                            stateFeatures[getattr(self, 'FRIEND'+str(idsOrder[i]+1)+'_X')],
                            stateFeatures[getattr(self, 'FRIEND'+str(idsOrder[i]+1)+'_Y')],
                            stateFeatures[getattr(self, 'FRIEND'+str(idsOrder[i]+1)+'_NUMBER')]
                                   ])
                #Finally sets the values
                for i in range(1,len(listProx)+1):
                     stateFeatures[getattr(self, 'FRIEND'+str(i)+'_GOAL_OPENING')] = copyList[i-1][0]
                     stateFeatures[getattr(self, 'FRIEND'+str(i)+'_OPP_PROXIMITY')] = copyList[i-1][1]
                     stateFeatures[getattr(self, 'FRIEND'+str(i)+'_PASS_OPENING')] = copyList[i-1][2]
                     stateFeatures[getattr(self, 'FRIEND'+str(i)+'_X')] = copyList[i-1][3]
                     stateFeatures[getattr(self, 'FRIEND'+str(i)+'_Y')] = copyList[i-1][4]
                     stateFeatures[getattr(self, 'FRIEND'+str(i)+'_NUMBER')] = copyList[i-1][5]
        #if there are two or more opponents
        if self.OPP2_X != None:
            listProx = []
            #Sort by euclidian distance
            for i in range(self.numberOpponents):
                   listProx.append(math.hypot(stateFeatures[getattr(self, 'OPP'+str(i+1)+'_X')]- stateFeatures[self.X_POSITION], 
                          stateFeatures[getattr(self, 'OPP'+str(i+1)+'_Y')]- stateFeatures[self.Y_POSITION]))
                            #Get list of friends' indexes in descending order according to proximity
            idsOrder = sorted(range(len(listProx)), key=lambda k: listProx[k])
                            #Get the sorted list and prepares the values to be changed
            copyList = []
            for i in range(len(listProx)):
                #Values from one of the friends
                copyList.append([
                        stateFeatures[getattr(self, 'OPP'+str(idsOrder[i]+1)+'_X')],
                        stateFeatures[getattr(self, 'OPP'+str(idsOrder[i]+1)+'_Y')],
                        stateFeatures[getattr(self, 'OPP'+str(idsOrder[i]+1)+'_NUMBER')]
                               ])
            #Finally sets the values
            for i in range(1,len(listProx)+1):
                 stateFeatures[getattr(self, 'OPP'+str(i)+'_X')] = copyList[i-1][0]
                 stateFeatures[getattr(self, 'OPP'+str(i)+'_Y')] = copyList[i-1][1]
                 stateFeatures[getattr(self, 'OPP'+str(i)+'_NUMBER')] = copyList[i-1][2]
                
        return stateFeatures
                    
          
    def get_friend_info(self,stateFeatures):
        """Returns a list containing all features corresponding to friendly agents.
        The return will be a list in which each position corresponds to an agent
        """
        
        friendInfo = []
        #Returns all attributes for each friend
        for i in range(self.numberFriends):
                    #Values from one of the friends
                    friendInfo.append([
                            stateFeatures[getattr(self, 'FRIEND'+str(i+1)+'_GOAL_OPENING')],
                            stateFeatures[getattr(self, 'FRIEND'+str(i+1)+'_OPP_PROXIMITY')],
                            stateFeatures[getattr(self, 'FRIEND'+str(i+1)+'_PASS_OPENING')],
                            stateFeatures[getattr(self, 'FRIEND'+str(i+1)+'_X')],
                            stateFeatures[getattr(self, 'FRIEND'+str(i+1)+'_Y')],
                            stateFeatures[getattr(self, 'FRIEND'+str(i+1)+'_NUMBER')]
                            ])
        
        
        return friendInfo
   
    def get_enemy_info(self,stateFeatures):
        """Likewise get_friend_info, returns a list containing features correspondings
        to enemy agents."""
        enemyInfo = []
        #Returns all attributes for each friend
        for i in range(self.numberOpponents):
                    #Values from one of the friends
                    enemyInfo.append([
                            stateFeatures[getattr(self, 'OPP'+str(i+1)+'_X')],
                            stateFeatures[getattr(self, 'OPP'+str(i+1)+'_Y')],
                            stateFeatures[getattr(self, 'OPP'+str(i+1)+'_NUMBER')]
                            ])
        
        
        return enemyInfo
    def get_independent_info(self,stateFeatures):
        """Returns the portion of the state that is not dependent on the number of 
          opponents and friends. An extra position is used in case at least one enemy
          is in the enviornment for the OPPONENT_PROXIMITY attribute"""
        independentInfo = []
        if self.numberOpponents > 0:
            independentInfo.append(stateFeatures[self.OPPONENT_PROXIMITY])
            
        independentInfo.extend([stateFeatures[self.X_POSITION],
                               stateFeatures[self.Y_POSITION],
                               stateFeatures[self.ORIENTATION],
                               stateFeatures[self.BALL_X],
                               stateFeatures[self.BALL_Y],
                               stateFeatures[self.ABLE_KICK],
                               stateFeatures[self.CENTER_PROXIMITY],
                               stateFeatures[self.GOAL_ANGLE],
                               stateFeatures[self.GOAL_OPENING]#,
                               #stateFeatures[self.LAST_ACTION_SUCESS]                               
                               ])
        
        return independentInfo
    
    def build_state(self,infoFriend,infoEnemies,infoIndependent):
        """Given all the features, creates a state for this state manager.
           The given features will be validated. In case of an invalid entry (in
           terms of number of features), an error will be thrown."""
        #Validating number of objects
        if len(infoFriend) != self.numberFriends:
            raise ValueError("A wrong number of parameters was specified for the 'build_state' function. "+
                              str(len(infoFriend))+" friend parameters informed, "+str(self.numberFriends)+" required.")
        if len(infoEnemies) != self.numberOpponents:
            raise ValueError("A wrong number of parameters was specified for the 'build_state' function. "+
                              str(len(infoEnemies))+" opponent parameters informed, "+str(self.numberOpponents)+" required.")
        if self.numberOpponents > 0:
            if len(infoIndependent) != 10:
                raise ValueError("A wrong number of parameters was specified for the 'build_state' function. "+
                              str(len(infoIndependent))+" opponent parameters informed, 11 required.")
        else:
            if len(infoIndependent) != 9:
                    raise ValueError("A wrong number of parameters was specified for the 'build_state' function. "+
                              str(len(infoIndependent))+" opponent parameters informed, 10 required.")
                    
        newState = [None]*(self.LAST_ACTION_SUCESS)
       
        #---- Independent Features
        if self.numberOpponents > 0:
           newState[self.OPPONENT_PROXIMITY] = infoIndependent[0]
           
        newState[self.X_POSITION] = infoIndependent[1]
        newState[self.Y_POSITION] = infoIndependent[2]
        newState[self.ORIENTATION] = infoIndependent[3]
        newState[self.BALL_X] = infoIndependent[4]
        newState[self.BALL_Y] = infoIndependent[5]
        newState[self.ABLE_KICK] = infoIndependent[6]
        newState[self.CENTER_PROXIMITY] = infoIndependent[7]
        newState[self.GOAL_ANGLE] = infoIndependent[8]
        newState[self.GOAL_OPENING] = infoIndependent[9]
        #newState[self.LAST_ACTION_SUCESS] = infoIndependent[10]
        
        #---- Friend Features
        for i in range(self.numberFriends):
             #Values from one of the friends
             newState[getattr(self, 'FRIEND'+str(i+1)+'_GOAL_OPENING')] = infoFriend[i][0]
             newState[getattr(self, 'FRIEND'+str(i+1)+'_OPP_PROXIMITY')] = infoFriend[i][1]
             newState[getattr(self, 'FRIEND'+str(i+1)+'_PASS_OPENING')] = infoFriend[i][2]
             newState[getattr(self, 'FRIEND'+str(i+1)+'_X')] = infoFriend[i][3]
             newState[getattr(self, 'FRIEND'+str(i+1)+'_Y')] = infoFriend[i][4]
             newState[getattr(self, 'FRIEND'+str(i+1)+'_NUMBER')] = infoFriend[i][5]
        #---- Enemy Features
        for i in range(self.numberOpponents):
             #Values from one of the friends
             newState[getattr(self, 'OPP'+str(i+1)+'_X')] = infoEnemies[i][0]
             newState[getattr(self, 'OPP'+str(i+1)+'_Y')] = infoEnemies[i][1]
             newState[getattr(self, 'OPP'+str(i+1)+'_NUMBER')] = infoEnemies[i][2]     
        #Now, the state is built
        return newState
                            
                  
            
    #-----------------------------------
    #Variables that are valid and are in the same position for all parameters
    #-----------------------------------
    #Agent's x-position
    X_POSITION = 0
    #Agent's y-position
    Y_POSITION = 1
    #Global direction
    ORIENTATION = 2
    #Ball x-position
    BALL_X = 3
    #Ball y-position
    BALL_Y = 4
    #Is the agent able to kick?
    ABLE_KICK = 5
    #Proximity to the center
    CENTER_PROXIMITY = 6
    #Angle from the agent to the center of the goal
    GOAL_ANGLE = 7
    #Largest open angle of the agent to the goal
    GOAL_OPENING = 8
      
    #------------------------------------
    # Possibly Invalid variables
    #-------------------------------------
    #Proximity to closest Opponent, invalid if there are no opponents
    OPPONENT_PROXIMITY = None  
    
    #Goal Oppenings
    FRIEND1_GOAL_OPENING = None
    FRIEND2_GOAL_OPENING = None
    FRIEND3_GOAL_OPENING = None
    FRIEND4_GOAL_OPENING = None
    
    #Proximities to closes opponent
    FRIEND1_OPP_PROXIMITY = None
    FRIEND2_OPP_PROXIMITY = None
    FRIEND3_OPP_PROXIMITY = None
    FRIEND4_OPP_PROXIMITY = None
    
    #Pass oppenings
    FRIEND1_PASS_OPENING = None
    FRIEND2_PASS_OPENING = None
    FRIEND3_PASS_OPENING = None
    FRIEND4_PASS_OPENING = None
    
    #For each friend: X, Y, and UNum
    FRIEND1_X = None
    FRIEND1_Y = None
    FRIEND1_NUMBER = None
    FRIEND2_X = None
    FRIEND2_Y = None
    FRIEND2_NUMBER = None
    FRIEND3_X = None
    FRIEND3_Y = None
    FRIEND3_NUMBER = None
    FRIEND4_X = None
    FRIEND4_Y = None
    FRIEND4_NUMBER = None
    
    #For each opponent: x,y and UNUM
    OPP1_X = None
    OPP1_Y = None
    OPP1_NUMBER = None
    OPP2_X = None
    OPP2_Y = None
    OPP2_NUMBER = None
    OPP3_X = None
    OPP3_Y = None
    OPP3_NUMBER = None
    OPP4_X = None
    OPP4_Y = None
    OPP4_NUMBER = None
    OPP5_X = None
    OPP5_Y = None
    OPP5_NUMBER = None
    
    #Chance of the last action being sucessfull
    LAST_ACTION_SUCESS = None
    
    
    
        
    def compile_variables(self):
       """Completes the index of each state variable"""
       nextUse = 9
       if self.numberOpponents > 0:
           self.OPPONENT_PROXIMITY = nextUse
           nextUse += 1
       #Variables related to friends
       
       #Goal Oppening
       if self.numberFriends > 0:
           self.FRIEND1_GOAL_OPENING = nextUse
           nextUse += 1
       if self.numberFriends > 1:
           self.FRIEND2_GOAL_OPENING = nextUse
           nextUse += 1
       if self.numberFriends > 2:
           self.FRIEND3_GOAL_OPENING = nextUse
           nextUse += 1
       if self.numberFriends > 3:
           self.FRIEND4_GOAL_OPENING = nextUse
           nextUse += 1           
           
       #Proximity to opponent
       if self.numberFriends > 0:
           self.FRIEND1_OPP_PROXIMITY = nextUse
           nextUse += 1
       if self.numberFriends > 1:
           self.FRIEND2_OPP_PROXIMITY = nextUse
           nextUse += 1
       if self.numberFriends > 2:
           self.FRIEND3_OPP_PROXIMITY = nextUse
           nextUse += 1
       if self.numberFriends > 3:
           self.FRIEND4_OPP_PROXIMITY = nextUse
           nextUse += 1  
           
       #Opening
       if self.numberFriends > 0:
           self.FRIEND1_PASS_OPENING = nextUse
           nextUse += 1
       if self.numberFriends > 1:
           self.FRIEND2_PASS_OPENING = nextUse
           nextUse += 1
       if self.numberFriends > 2:
           self.FRIEND3_PASS_OPENING = nextUse
           nextUse += 1
       if self.numberFriends > 3:
           self.FRIEND4_PASS_OPENING = nextUse
           nextUse += 1  
        
       #X,Y, and UNUM of friends
       if self.numberFriends > 0:
           self.FRIEND1_X = nextUse
           self.FRIEND1_Y = nextUse + 1
           self.FRIEND1_NUMBER = nextUse + 2
           nextUse += 3
       if self.numberFriends > 1:
           self.FRIEND2_X = nextUse
           self.FRIEND2_Y = nextUse + 1
           self.FRIEND2_NUMBER = nextUse + 2
           nextUse += 3
       if self.numberFriends > 2:
           self.FRIEND3_X = nextUse
           self.FRIEND3_Y = nextUse + 1
           self.FRIEND3_NUMBER = nextUse + 2
           nextUse += 3
       if self.numberFriends > 3:
           self.FRIEND4_X = nextUse
           self.FRIEND4_Y = nextUse + 1
           self.FRIEND4_NUMBER = nextUse + 2
           nextUse += 3
           
           
           
       #X,Y, and NUM of opponents
       if self.numberOpponents > 0:
           self.OPP1_X = nextUse
           self.OPP1_Y = nextUse + 1
           self.OPP1_NUMBER = nextUse + 2
           nextUse += 3
       if self.numberOpponents > 1:
           self.OPP2_X = nextUse
           self.OPP2_Y = nextUse + 1
           self.OPP2_NUMBER = nextUse + 2
           nextUse += 3
       if self.numberOpponents > 2:
           self.OPP3_X = nextUse
           self.OPP3_Y = nextUse + 1
           self.OPP3_NUMBER = nextUse + 2
           nextUse += 3
       if self.numberOpponents > 3:
           self.OPP4_X = nextUse
           self.OPP4_Y = nextUse + 1
           self.OPP4_NUMBER = nextUse + 2
           nextUse += 3
       if self.numberOpponents > 4:
           self.OPP5_X = nextUse
           self.OPP5_Y = nextUse + 1
           self.OPP5_NUMBER = nextUse + 2
           nextUse += 3
           
       self.LAST_ACTION_SUCESS = nextUse