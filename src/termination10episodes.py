#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 09:53:42 2017

Terminates when the cummulative reward looks the same for 10 consecutive episodes
@author: Felipe Leno
"""

from terminationcondition import TerminationCondition

class Termination10Episodes(TerminationCondition):
    
    tolerance = 0.01 #Tolerance in % of cummulative reward differences
    limitation = 10 #Maximum number of episodes per task
    consecutive = 2
    currentEpisode = 1
    rewardList = []
    currentSumReward = 0
    finished = False
    
    
    def keep_training(self,task,target_task,curriculum,episodes,steps,totalEpisodes,totalSteps,parameter):
        """Defines if the agent should keep training in the current task.
            task: CUrrent task
            target_task: Target task
            curriculum: The curriculum learning algorithm
            episodes: number of episodes executed for this task
            steps: number of steps for this class
            totalEpisodes: Total number of episodes since the beginning of training
            totalSteps: Total number of executed steps
            parameter: Experiment parameters
        """
        
        return not self.finished
    def init_task(self):
        """Resets for a new task"""
        self.rewardList = []
        self.currentSumReward = 0
        self.currentEpisode = 1
        self.finished = False
        
    
    
    def observe_step(self,state,action,statePrime,reward):
        """Computer the reward in the sum for the current episode"""
        self.currentSumReward += reward
    
    def finish_episode(self):
        """Compares if the last 10 episodes had the same reward"""
        
        self.currentEpisode += 1
        
        if self.currentEpisode > self.limitation:
             self.finished = True
             return 
        #Add new episode information
        if len(self.rewardList)==self.consecutive:
            self.rewardList.pop()
        self.rewardList.insert(0,self.currentSumReward)
        
        self.currentSumReward = 0
        
        #Check differences
        i = 0
        #If the difference of the last 10 episodes is smaller than the tolerance
        # the training is over
        if len(self.rewardList)==self.consecutive:
            finish = True
            while finish and i<self.consecutive-1:
                
                for j in range(i+1,self.consecutive):
                    dif = abs(self.rewardList[i] - self.rewardList[j])
                    if dif > abs(self.rewardList[i])*self.tolerance:
                        finish = False
                i += 1
        else:
            finish = False
            
        self.finished = finish
                    
        
