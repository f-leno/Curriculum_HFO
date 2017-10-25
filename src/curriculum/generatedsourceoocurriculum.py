#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 14:34:07 2017
Code to automaticaly generate source tasks and build a curriculum
@author: Felipe Leno
"""


from curriculum.objectorientedcurriculum import ObjectOrientedCurriculum

import os
import random
import copy
import math
import numpy as np


class GeneratedSourceOOCurriculum(ObjectOrientedCurriculum):
    
    workFolder = None
    target_task = None
    repGeneration = None
    
    
    def generate_curriculum(self,target_task, sourceFolder,workFolder,thresholdTask = 2,repGeneration = 10):
        self.workFolder = workFolder 
        self.target_task = target_task
        self.repGeneration = repGeneration
        
        super(GeneratedSourceOOCurriculum,self).generate_curriculum(target_task=target_task,sourceFolder=sourceFolder,
             workFolder=workFolder,thresholdTask=thresholdTask)
    def generate_curriculum_from_tasks(self,target_task, taskList,thresholdTask = 3.2):
        super(GeneratedSourceOOCurriculum,self).generate_curriculum_from_tasks(target_task=target_task,taskList=taskList,
             thresholdTask=thresholdTask)
        
    def read_folder(self,sourceFolder):
        """Instead of reading aq sorce folder, the source tasks are generated."""
       
        self.generate_tasks(sourceFolder)     
              
        return super(GeneratedSourceOOCurriculum,self).read_folder(self.workFolder)
     
    def generate_tasks(self,sourceFolder):

       
       
       random.seed(self.seed)
       
       #Erases all previous tasks in temp folder
       if not os.path.exists(self.workFolder):
           os.makedirs(self.workFolder)
       dirContent=os.listdir(self.workFolder)
       for item in dirContent:
           if item.endswith(".task"):
               os.remove(self.workFolder+ item)
               
       if self.target_task.get_domain_task() == "HFOTask":
           self.generate_hfo()
       else:
            self.generate_gridworld()
       
    def generate_hfo(self):
        """Generates the set of source tasks for the hfo domain"""
              #Simplify function in the algorithm
        #In this case the simple set is the distance
        simpleSet = []
        
        dist = self.target_task.distance
        
        #Generate various distances
        for i in np.arange(dist,1.0,0.2):
            simpleSet.append(i)
        
        numFriends = self.target_task.numberFriends
        numEnemies = self.target_task.numberEnemies
        
        #Generates tasks as in the algorithm
        for i in range(self.repGeneration):
           for y in range(0,min(numFriends,numEnemies)+1):
               #Draw q objects from each class
               if numFriends > numEnemies:
                    numFriends = random.choice(range(y,numFriends+1))
                    numEnemies = random.choice(range(0,numEnemies+1))
               else:
                    numFriends = random.choice(range(0,numFriends+1))
                    numEnemies = random.choice(range(y,numEnemies+1))
               
               #Draw F from Fsimple
               distance = random.choice(simpleSet)
               enStrategy = self.target_task.strategy
               #Stores state in file
               state = str(numFriends) + ";" + str(numEnemies) + ";" + enStrategy + ";" + str(distance) + ";" + str(random.randint(0,1000))
               
               fileName = self.workFolder + "friends_" + str(numFriends) + '_enemies_' + str(numEnemies) + '_dist_' + str(int(distance*10)) + enStrategy + '.task'
               with open(fileName,'w') as opFile:
                   opFile.write(state)
                   opFile.close()
        
    def generate_gridworld(self):
        """Generates the set of source tasks for the GridWorld domain."""
        #Simplify function in the algorithm
        simpleSet = [
                        [5,5],
                        #[2,2],
                        [3,3],
                        [7,7],
                        #[5,1],
                        #[1,5]
                    ]
        num_fires = self.target_task.num_fires()
        num_pits = self.target_task.num_pits()
       
        
        allTreasures,allPits,allFires = self.split_state(self.target_task.init_state())
       

       
        #Generates tasks as in the algorithm
        for i in range(self.repGeneration):
           for y in range(0,min(num_fires,num_pits)+1):
               #Draw q objects from each class
               if num_fires > num_pits:
                    qPit = random.choice(range(y,num_pits+1))
                    qFire = random.choice(range(0,num_fires+1))
               else:
                    qPit = random.choice(range(0,num_pits+1))
                    qFire = random.choice(range(y,num_fires+1))
               
               #Draw F from Fsimple
               taskSize = random.choice(simpleSet)
               

               listPits = random.sample(allPits,qPit)
               listFires = random.sample(allFires,qFire)
               
               #Stores state in file
               state = self.build_init_state(taskSize,allTreasures,copy.copy(listPits),copy.copy(listFires))
               
               fileName = self.workFolder + str(taskSize[0]) + "," + str(taskSize[1]) + ',' + str(i) + ' - fire' + str(qFire) + ' - pit' + str(qPit) + '.task'
               with open(fileName,'w') as opFile:
                   opFile.write(state)
                   opFile.close()
        
            
    def build_init_state(self,taskSize,allTreasures,allPits,allFires):
        """Builds the initial state and returns it in textual format"""
        
        #Agent initial position is in the middle of the grid
        agPosic = [int(math.ceil(float(taskSize[0])/2)),int(math.ceil(float(taskSize[0])/2))]
        #Already used positions
        selectedObjs = [agPosic,[taskSize[0],taskSize[1]]]
        okPit = []
        okFire = []
        
        #Verifies if object positions are valid
        for pit in allPits:
            #Check if there is any available position:
            if len(selectedObjs) == taskSize[0] * taskSize[1]:
                continue
            #Sorts new positions until a free one is found
            while pit in selectedObjs or pit[0]>taskSize[0] or pit[1]>taskSize[1]:
                pit[0] = random.choice(range(1,taskSize[0]+1))
                pit[1] = random.choice(range(1,taskSize[1]+1))
            selectedObjs.append(pit)
            okPit.append(pit)
            
        #The same procedure is done with fire objects
        for fire in allFires:
            #Check if there is any available position:
            if len(selectedObjs) == taskSize[0] * taskSize[1]:
                continue
            #Sorts new positions until a free one is found
            while fire in selectedObjs or fire[0]>taskSize[0] or fire[1]>taskSize[1]:
                fire[0] = random.choice(range(1,taskSize[0]+1))
                fire[1] = random.choice(range(1,taskSize[1]+1))
            selectedObjs.append(fire)
            okFire.append(fire)
        #builds text of initial state
        # task size
        textState = str(taskSize[0])+";"+str(taskSize[1])+";" 
        #Agent always in the same position
        textState += "agent:"+str(agPosic[0])+"-"+str(agPosic[1])+",treasure:" + str(taskSize[0]) + "-" + str(taskSize[1])
        
        for pit in okPit:
            textState += ",pit:" + str(pit[0]) + "-" + str(pit[1])
        
        for fire in okFire:
            textState += ",fire:" + str(fire[0]) + "-" + str(fire[1])
        
        return textState
        
            
        
    def split_state(self,initState):
        """Given a description of the initial state, builds lists of:
        treasures,pits,fires"""
        
        fires = []
        pits = []
        treasures = []
        
        for obj in initState:
            if obj[0] == 'fire':
                fires.append([obj[1],obj[2]])
            elif obj[0] == 'pit':
                pits.append([obj[1],obj[2]])
            elif obj[0] == 'treasures':
                pits.append([obj[1],obj[2]])
        return treasures,pits,fires
                
        
        
          

        
        
        
        
        
    
                
        
        
                
                
            




