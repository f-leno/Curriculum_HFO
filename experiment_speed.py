#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 12:06:11 2017
Experiment to evaluate speed of Curriculum Generation
(the output will be on the console)
@author: Felipe Leno
"""


#Generate random task for HFO as well
import argparse
import sys
import random
from domain.hfotask import HFOTask
from domain.gridworldtask import GridWorldTask
from timeit import default_timer as timer
#from cmac import CMAC


#from agents.agent import Agent

  


def get_args():
    """Arguments for the experiment
            --initial_size: Initial Curriculum Size to be evaluated
            --end_size: Last curriculum Size to be evaluated
            --interval_size: Interval of evaluations
            --curriculum_alg: Curriculum algorithm to be evaluated
            
    
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--initial_size',type=int,  default=10)
    parser.add_argument('-e','--end_size',type=int,  default=500) 
    parser.add_argument('-s','--seed',type=int,  default=0)
    parser.add_argument('-is','--interval_size',type=int, default=10)
    parser.add_argument('-a','--curriculum_alg',default='ObjectOrientedCurriculum')
    parser.add_argument('-do','--domain',choices=['GridWorld','HFODomain'],default="HFODomain")
     

    return parser.parse_args()

   
    
def build_object():
    """Builds the object specified in the argument 
    """
     
    parameter = get_args()
    
   

    curriculumName = getattr(parameter,"curriculum_alg")
    print ("Curriculum: "+curriculumName)
    try:
            CurriculumClass = getattr(
               __import__('curriculum.' + (curriculumName).lower(),
                          fromlist=[curriculumName]),
                          curriculumName)
    except ImportError as error:
            print error
            sys.stderr.write("ERROR: missing python module: " +curriculumName + "\n")
            sys.exit(1)
        
    CURRICULUM = CurriculumClass(seed=parameter.seed,agent = None)
    
    
     
    return CURRICULUM
    
def generate_target(parameter):
    """Gerates a target task"""
    task = None
    if parameter.domain == 'GridWorld':
        taskData = "10;10;agent:1-1,fire:8-3,fire:9-3,fire:10-3,fire:10-5,fire:2-5,fire:6-6,fire:9-8,fire:10-8,pit:1-3,pit:2-3,pit:3-3,pit:4-3,pit:5-3,pit:7-3,pit:5-5,pit:7-5,pit:6-8,pit:8-8,pit:7-10,treasure:10-10"
        task = GridWorldTask(taskName='target',taskData=taskData)
    elif parameter.domain == "HFODomain":
        taskData = "4;4;helios;0.3;123"
        task = HFOTask(taskName='target', taskData=taskData)
def generate_random_task():
    """Gerates a random task data"""
    taskData = ""
    possibleX = [2,3,5,7,10]
    possibleY = [2,3,5,7,10]
    possibleNumFire = range(10)
    possibleNumPit = range(10)
    
    #Random grid Size
    randX = random.choice(possibleX)
    randY = random.choice(possibleY)
    
    #including in task data
    taskData += str(randX)+";"+str(randY)+";agent:1-1;treasure:"+ str(randX)+"-"+str(randY)
    
    #Random fire and pit positions
    numFire = random.choice(possibleNumFire)
    numPit = random.choice(possibleNumPit)
    
    #Generate fires
    for i in range(numFire):
        x = random.choice(range(1,randX+1))
        y = random.choice(range(1,randY+1))
        taskData += ',fire:'+str(x)+"-"+str(y)
    #Generate pits
    for i in range(numPit):
        x = random.choice(range(1,randX+1))
        y = random.choice(range(1,randY+1))
        taskData += ',pit:'+str(x)+"-"+str(y)
        
    return taskData

def add_tasks(taskList,numberTasks):
    """Generates n random tasks"""
    for i in range(numberTasks):
        randomTask = generate_random_task()
        taskList.append(Task(taskName=str(len(taskList)+1),taskData=randomTask))
    return taskList
def main():
    parameter = get_args()
    print parameter
   
    random.seed(parameter.seed)
    target_task = generate_target(parameter)

    taskList = []
    for currentSize in range(parameter.initial_size,parameter.end_size+1,parameter.interval_size):

        
        curriculum = build_object()
        random.seed(parameter.seed + currentSize)
        taskList = add_tasks(taskList,parameter.interval_size)

        start = timer()
        #Generate Curriculum for target task
        curriculum.generate_curriculum_from_tasks(target_task, taskList)
        
        end = timer()
        print("Size: "+str(currentSize)+ "-------" + str(end - start))   
    

    
    
    

if __name__ == '__main__':
    main()
