#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 13:52:49 2017
Builds a Curriculum with only the target task (regular learning)
@author: Felipe Leno
"""

from curriculum.curriculum import Curriculum

class NoneCurriculum(Curriculum):
    """ This is the base class for all Curriculum Learning implementations.

    """
    target_task = None
    usedTask = True
    
   
    def __init__(self, seed=12345,agent=None):
        super(NoneCurriculum, self).__init__(seed=seed,agent=agent)
        
    
    def generate_curriculum(self,target_task, sourceFolder,workFolder):
        """ The Curriculum is generated by this function (stored internally) """
        self.target_task = target_task
        self.usedTask = False        
    
    def empty_curriculum(self):
        """ Returns if the curriculum already has returned the task """
        return self.usedTask
    
    
    def draw_task(self):
        """ Returns the previously given task"""
        self.usedTask = True
        return self.target_task
    def previous_tasks(self):
        return []

    def generate_curriculum_from_tasks(self,target_task, taskList):
        self.target_task = target_task
        self.usedTask = False    
    def print_result(self):
        """Prints the CUrriculum"""
        pass
