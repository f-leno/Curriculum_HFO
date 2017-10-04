#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 09:40:34 2017
THis class is used as termination condition for a task in the HFODOmain.

The learning process will be interrupted if the average score in the last 10 episodes is 50%, or if no goal
was scored in the last 30 episodes
@author: Felipe Leno
"""



from terminationcondition import TerminationCondition

class HFOTermination(TerminationCondition):
    
    limitation = 200 #Maximum number of episodes per task
    limitNoGoal = 30 #Maximum number of episodes without goals
    evaluateWindow = 10 #number of episodes to count goal percentage
    thresholdGoal = 0.7 #Percentage to stop training
    currentEpisode = 1 
    goalList = []
    lastReward = 0
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
        self.goalList = []
        self.lastReward = 0
        self.currentEpisode = 1
        self.finished = False
        
    
    
    def observe_step(self,state,action,statePrime,reward):
        """Computer the reward in the sum for the current episode"""
        self.lastReward = reward
    
    def finish_episode(self):
        """Compares if the last 10 episodes had the same reward"""
        
        self.currentEpisode += 1
        
        
        if self.currentEpisode > self.limitation:
             self.finished = True
             return 
        #Add new episode information
        if self.lastReward > 0: #Goal
            self.goalList.append(True)
        else:
            self.goalList.append(False)
        
        #print("------ Episode "+str(self.currentEpisode-1)+" goal: "+str(self.goalList[len(self.goalList)-1]))
            
        #At least 10 training episodes before interrupting learning
        if len(self.goalList) >= self.evaluateWindow:
            #Get the last 10 episodes
            lastWindow = self.goalList[len(self.goalList)-self.evaluateWindow:]
            goalPercent = lastWindow.count(True) / self.evaluateWindow
            #Is the goal percent enough to stop training?
            if goalPercent >= self.thresholdGoal:
                self.finished = True
                return
                
        
        #Check now the limit of episodes wihtout goals
        if len(self.goalList) >= self.limitNoGoal:
            lastWindow = self.goalList[len(self.goalList)-self.limitNoGoal:]
            #Check if at least one goal exists
            goalExists = next((x for x in lastWindow if x), False)
            if not goalExists:
                self.finished = True
                return
            
            
        self.finished = False
                    
        
