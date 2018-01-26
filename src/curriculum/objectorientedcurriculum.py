#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:55:07 2017
Implementation of the Object-Oriented Curriculum Generation (with given source tasks)
@author: Felipe Leno
"""


from curriculum.svetlikcurriculum import SvetlikCurriculum

import OOUtil


class ObjectOrientedCurriculum(SvetlikCurriculum):
    
    def generate_curriculum(self,target_task, sourceFolder,workFolder,thresholdTask = None):
        # Defines default parameter to each domain
        if thresholdTask is None:
            if target_task.get_domain_task() == 'HFOTask':
                thresholdTask = 3.2
            elif target_task.get_domain_task() == 'GridWorldTask':
                thresholdTask = 42#40
        super(ObjectOrientedCurriculum,self).generate_curriculum(target_task=target_task,sourceFolder=sourceFolder,
             workFolder=workFolder,thresholdTask=thresholdTask)
    def generate_curriculum_from_tasks(self,target_task, taskList,thresholdTask = None):
        # Defines default parameter to each domain
        if thresholdTask is None:
            if target_task.get_domain_task() == 'HFOTask':
                thresholdTask = 3.2
            elif target_task.get_domain_task() == 'GridWorldTask':
                thresholdTask = 42
        super(ObjectOrientedCurriculum,self).generate_curriculum_from_tasks(target_task=target_task,taskList=taskList,
             thresholdTask=thresholdTask)
        
          
    def transfer_potential(self,currentTask,target_task,curriculumTasks):
        """The transfer potential is now calculated through object-based metrics"""
        simSource = OOUtil.task_similarity(currentTask,target_task)
        
        if len(curriculumTasks) > 0:
            simMax = max(curriculumTasks,key=lambda t:OOUtil.task_similarity(currentTask,t))
            simMax = OOUtil.task_similarity(currentTask,simMax)
            #Avoiding division by zero
            simMax = simMax if simMax > 0 else 1
        else:
            simMax = 1
        
        
        
        sizeStateSpaceSource = currentTask.state_space()
        sizeStateSpaceTarget = target_task.state_space()
        
        numObjSource = currentTask.number_objects()
        numObjTarget = target_task.number_objects()
                      
        transferPot = simSource / (simMax * (sizeStateSpaceSource*(numObjSource+1)) / (sizeStateSpaceTarget*(numObjTarget+1)))
        #transferPot = simSource / (simMax * sizeStateSpaceSource / sizeStateSpaceTarget)
        return transferPot
        
        
        
        
        
    
                
        
        
                
                
            


