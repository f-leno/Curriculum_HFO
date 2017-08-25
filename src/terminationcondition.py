#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 09:21:16 2017
This class contols the termination of tasks
@author: Felipe Leno
"""
import abc

class TerminationCondition(object):

    __metaclass__ = abc.ABCMeta
    
   
    def __init__(self):
        pass
        
        

    @abc.abstractmethod
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
        pass  
    
    @abc.abstractmethod
    def observe_step(self,state,action,statePrime,reward):
        """Notifies the termination condition controller of a new step"""
        pass
    @abc.abstractmethod   
    def finish_episode(self):
        """Notifies the termination condition controller of the end of an episode"""
        
    @abc.abstractmethod   
    def init_task(self):
        """Notifies the Creation of a new task"""
        
        
 




