#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:55:07 2017
Implementation of the Object-Oriented Curriculum Generation (with given source tasks)
@author: Felipe Leno
"""

from __future__ import division
from svetlikcurriculum import SvetlikCurriculum

import OOUtil


class ObjectOrientedCurriculum(SvetlikCurriculum):
    
    def generate_curriculum(self,target_task, sourceFolder,workFolder,thresholdTask = 4):
        super(ObjectOrientedCurriculum,self).generate_curriculum(target_task=target_task,sourceFolder=sourceFolder,
             workFolder=workFolder,thresholdTask=thresholdTask)
    def generate_curriculum_from_tasks(self,target_task, taskList,thresholdTask = 3.2):
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
        
        
        
        sizeStateSpaceSource = currentTask.get_sizeX() * currentTask.get_sizeY() 
        sizeStateSpaceTarget = target_task.get_sizeX() * target_task.get_sizeY()
        
        numObjSource = currentTask.num_pits() + currentTask.num_fires()
        numObjTarget = currentTask.num_pits() + currentTask.num_fires()
                      
        transferPot = simSource / (simMax * (sizeStateSpaceSource*(numObjSource+1)) / (sizeStateSpaceTarget*(numObjTarget+1)))
        #transferPot = simSource / (simMax * sizeStateSpaceSource / sizeStateSpaceTarget)
        return transferPot
        
        
        
        
        
    
                
        
        
                
                
            


