#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 11:01:41 2017
Environment Class for preparing HFO experiments
@author: Felipe Leno
"""

from domain.domain import Domain
#from domain import Domain

import domain.portmanager as portmanager
#import portmanager as portmanager

import subprocess
import domain.hfoactions as hfoactions
#import hfoactions as hfoactions

from domain.hfostate import HFOStateManager
#from hfostate import HFOStateManager

import hfo
#from domain.hfotask import HFOTask
from domain.hfotask import HFOTask
import time,sys,math
from threading import Thread

class HFODomain(Domain):
    
    def build_environment(self,taskFile,limitSteps,taskName = None):
        """Instantiates an object representing the task in this domain.
            --taskFile = The path for a file containing the description of a task in this domain
            --limitSteps = The maximum number of steps to be executed per episode.
            --taskName = optional parameter defining the task name.
            returns:
                --task: The task according to the given file.
        """
        #Building the task
        task = HFOTask(filePath=taskFile,taskName=taskName)
        
        #Bulding the enviornment
        #environment = HFOEnv(taskParam = task.task_features(),limitFrames = limitSteps)
        
        return task
        
       
    def build_environment_from_task(self,task,limitSteps):
        """Builds the environment from previously built tasks.
           --task = The Task Object
           --limitSteps = The maximum number of steps to be executed per episode.
           returns:
               --environment: The desired environment
        """
        #Bulding the enviornment
        environment = HFOEnv(taskParam = task.task_features(),limitFrames = limitSteps)
        
        return environment
    
    
class HFOEnv(object):
    serverPort = None
    hfoObj = None
    #Path for the bin folder
    serverPath = "../HFO/bin/"#'/home/leno/gitProjects/Curriculum_HFO/HFO/bin/'#"../HFO/bin/"
    #Server subprocess to be finished later
    serverProcess = None
    clientProcess = None

    #Status of the last step
    lastStatus = None
    #Total number of episodes
    totalEpisodes = None
    #Total number of goals
    goals = None
    #Number of friendly agents
    numberFriends = None
    #Number of Opponents
    numberOpponents = None
    #Utilities for state space variables
    stateSpaceManager = None
    #Last applied action
    lastAction = None
    #Terminate Server thread?
    terminateThread = None
    #Action and parameter  to be sent to HFO server
    applyAction = None
    actionParameter = None
    #Variable to request step processing to another thread
    stepRequest = None
    #Variable to control when to erase other threads
    clearServer = None
    
    
    
    def __init__(self,taskParam,limitFrames = 200):
        """Initiates the HFO environment"""
        #Returns a port that is not being used
        self.serverPort = portmanager.get_free_port()
        #self.serverPort = 2000
        self.numberFriends = taskParam[0]
        self.numberOpponents =  taskParam[1]
        
        self.hfoObj = hfo.HFOEnvironment()
        
        self.stepRequest = False
        self.clearServer = False
        #self.init_server(taskParam,limitFrames)
        
        
        #Initiates a new thread only to avoid an error when loading the strategy.cpp file
        self.terminateThread = False
        t = Thread(target=init_server, args=(self,taskParam,limitFrames))
        t.start()
        t.join()
        
        time.sleep(2)
        
        #Initiates a new thread to create the server
        t = Thread(target=connect_server, args=(self,))
        t.start()
        time.sleep(1)
        #The connection with the server is OK after here.
        
        self.totalEpisodes = 0
        self.goals = 0
        
        self.stateSpaceManager = HFOStateManager(self.numberFriends,self.numberOpponents)
 
        
    def clean_connections(self):
        """Cleans all the initiated services and files"""
        self.clearServer = True
        #Wait until another thread finishes the HFO client
        while self.clearServer:
            pass
        
        #Kill the HFO server
        subprocess.call("kill -9 -"+str(self.serverProcess.pid), shell=True)
        for proc in self.clientProcess:
            subprocess.call("kill -9 -" + str(proc.pid), shell=True)

        time.sleep(2)
        #portmanager.release_port(self.serverPort)
        
    def finish_learning(self):
        self.clean_connections()
        

    
    def all_actions(self,forExploration=False):
        """Returns the set of applicable actions for the agent
           in case the agent has the ball, a PASS for each friend, DRIBBLE and SHOOT
           are applicable. Otherwise, only MOVE is applicable
        """
        fullState = self.hfoObj.getState()
        withBall = fullState[self.stateSpaceManager.ABLE_KICK] == 1.0
                
        return hfoactions.all_actions(self.numberFriends, withBall, forExploration)  
        
    def act(self,action):
        """Performs the agent action"""
        #Transforms the action in the agent's point of view to the correct HFO server format
        self.lastAction = action
        self.applyAction, self.actionParameter = self.translate_action(action, self.hfoObj.getState())
        #Wait for another thread
        while not self.applyAction is None:
            pass

        
    def translate_action(self, action, stateFeatures):
        """Translates the action to one that is understandable in the HFO server"""
        #If the agent chooses a pass action, a translation is needed
        if hfoactions.is_pass_action(action):
            #According to the chosen action, defines which of the agents is the destination of the pass
            # index=0 corresponds to the closest agent, while index=1 to the second closest, and etc.
            indexAction = hfoactions.pass_index(action)
            f = self.stateSpaceManager
            #Sort Friends by euclidian distance
            listProx = [math.hypot(stateFeatures[f.FRIEND1_X]- stateFeatures[f.X_POSITION], 
                                   stateFeatures[f.FRIEND1_Y]- stateFeatures[f.Y_POSITION])]
            listIDs =  [stateFeatures[f.FRIEND1_NUMBER]]
            
            if self.numberFriends > 1:
                listProx.append(math.hypot(stateFeatures[f.FRIEND2_X]- stateFeatures[f.X_POSITION], 
                                   stateFeatures[f.FRIEND2_Y]- stateFeatures[f.Y_POSITION]))
                listIDs.append(stateFeatures[f.FRIEND2_NUMBER])
                
                if self.numberFriends > 2:
                    listProx.append(math.hypot(stateFeatures[f.FRIEND3_X]- stateFeatures[f.X_POSITION], 
                                   stateFeatures[f.FRIEND3_Y]- stateFeatures[f.Y_POSITION]))
                    listIDs.append(stateFeatures[f.FRIEND3_NUMBER])
                    
                    if self.numberFriends > 3:
                        listProx.append(math.hypot(stateFeatures[f.FRIEND4_X]- stateFeatures[f.X_POSITION], 
                                   stateFeatures[f.FRIEND4_Y]- stateFeatures[f.Y_POSITION]))
                        listIDs.append(stateFeatures[f.FRIEND4_NUMBER])
            #Get list of friends' indexes in descending order according to proximity
            idsOrder = sorted(range(len(listProx)), key=lambda k: listProx[k])
            #To whom the agent should pass
            indexFriend = idsOrder[indexAction]
            #Id according to HFO internal code
            friendUNum = listIDs[indexFriend]
            actionRet = hfo.PASS
            argument = friendUNum                                                        
        else:
            actionRet = action
            argument = None
        if hfo.PASS == actionRet and argument is None or argument == 0:
            print(action)
            print(stateFeatures)
            print(self.numberFriends)
        return actionRet, argument  
      
    def step(self):
        """Performs the state transition and returns (statePrime.action,reward)"""   
        self.stepRequest = True
        #Wait until another thread completes the step
        while self.stepRequest:
            pass
        
        statePrime = self.get_state()
        action = self.lastAction
        reward = self.observe_reward()
        return (statePrime,action,reward)
        
    def check_terminal(self):
        """Checks if the current state is terminal and processes the reward"""
        #Here, there is no need to check the environment status. Then, we use the method
        #to count the number of goals
        if self.lastStatus != hfo.IN_GAME:
            self.totalEpisodes += 1
            if self.lastStatus == hfo.GOAL:
                self.goals += 1
        
    def get_state(self):
        """Returns the state in the point of view of the agent. 
        The state features are filtered from the full set of features in the HFO server.
        """
        return self.filter_features(self.hfoObj.getState())
    
    def filter_features(self,stateFeatures):
        """Removes the irrelevant features from the HFO standard feature set"""   
        stateFeatures = self.stateSpaceManager.reorderFeatures(stateFeatures)
        return self.stateSpaceManager.filter_features(stateFeatures)


    def observe_reward(self):
        """Returns the reward for the agent"""
        if(self.lastStatus == hfo.IN_GAME):
            return 0.0
        elif(self.lastStatus == hfo.CAPTURED_BY_DEFENSE):
             return -1.0
        elif(self.lastStatus == hfo.OUT_OF_BOUNDS):
             return -1.0
        elif(self.lastStatus == hfo.OUT_OF_TIME):
             return 0.0
        elif(self.lastStatus == hfo.GOAL):
             return 1.0
        else:
            print("%%%%% Strange HFO STATUS: "+hfo.statusToString(self.lastStatus))
        
        return 0.0
    
    def is_terminal_state(self):
        """Returns if the current state is terminal"""
        return not self.lastStatus == hfo.IN_GAME
    
    def start_episode(self):
        """Start next evaluation episode"""
        self.lastStatus = hfo.IN_GAME
        self.applyAction = None
        self.actionParameter = None
        
    def load_episode(self,episodeInfo):
        """For this domain the server performs the reset
        """
        pass
    def state_transition(self):
        """Executes the state transition""" 
        pass
    
"""class ClientConnection():
    hfoObj = None
    main = None
    def __init__(self,main):
        self.main = main
        self.hfoObj = self.main.hfoObj
        
    def clear(self):
        self.hfoObj.act(hfo.QUIT)
    def action(self,action,parameter):
        if parameter is None:
                self.hfoObj.act(action)
        else:
                self.hfoObj.act(action, parameter)
    def step(self):
        self.main.lastStatus = self.hfoObj.step()"""
    
def connect_server(self):
        """Connects the client subprocess in the hfo server
            The learning process should be all executed in here because of strange
            errors in the HFO server when executing more than one client at the same time
        """
        #Path with formations file
        connectPath = self.serverPath+'teams/base/config/formations-dt'
        
        #Connecting in the server
        serverResponse = self.hfoObj.connectToServer(
                feature_set= hfo.HIGH_LEVEL_FEATURE_SET,
                config_dir=connectPath,
                server_port=self.serverPort,
                server_addr='localhost',
                team_name='base_left',
                play_goalie=False)
        print("%%%% Server connection FeedBack:    " + str(serverResponse))
       
        while not self.clearServer:
            #Wait until one action is chosen
            while self.applyAction is None and not self.clearServer:
                #print("Waiting action")
                time.sleep(0.0001)
            #Verifies if the agent should stop learning
            if self.clearServer:
                continue
                    
                
            #Send action to HFO server.
            if self.actionParameter is None:
                self.hfoObj.act(self.applyAction)
            else:
                self.hfoObj.act(self.applyAction, self.actionParameter)
             
            self.applyAction = None
            self.actionParameter = None
            #Perform HFO step
            while not self.stepRequest and not self.clearServer:
                time.sleep(0.0001)
            #Should the agent stop learning?
            if self.clearServer:
                continue
                
            self.lastStatus = self.hfoObj.step()
            if(self.lastStatus == hfo.SERVER_DOWN):
                self.hfoObj.act(hfo.QUIT)
                print("%%%%%%% HFO Server Down, Ending Environment")
                sys.exit(0)  
            self.stepRequest = False
        #When the clearServer is set as true, it is time to close the connection
        self.hfoObj.act(hfo.QUIT)
        self.clearServer = False
                
            
            
        
def init_server(self,taskParam,limitFrames):
        """Initiates the server process. Possible task parameters:
           [0] - number of agents in the same team - from 0 to 4
           [1] - number of agents in the other team - from 0 to 5
           [2] - strategy of the enemy team - 'base','helios'
           [3] - avg initial distance from goal - from 0 to 1
           [4] - seed for server
           [5] - Boolean indicating if all the players are npcs
            
        """
        numberFriends   = taskParam[0]
        numberOpponents = taskParam[1]
        opStrategy      = taskParam[2]
        avgDist         = taskParam[3]
        seed            = taskParam[4]
        
        
        

        
          #p.add_argument('--ball-x-min', dest='min_ball_x', type=float, default=0.0,
          #       help='Ball initialization min x position: [0,1]. Default: 0')
          #p.add_argument('--ball-x-max', dest='max_ball_x', type=float, default=0.2,
          #       help='Ball initialization max x position: [0,1]. Default: .2')
        
        #Computes min/max distance of the initialization according to avgDist
        xMin = avgDist - 0.1
        xMax = avgDist + 0.1
        
        #Build all commands correspondent to parameters
        #agentsParam = " --offense-agents 1 --offense-npcs "+str(numberFriends)
        agentsParam = " --offense-agents "+str(numberFriends+1)+" --offense-npcs 0"
        opponentsParam = " --defense-npcs "+str(numberOpponents)
        opStrategy = " --offense-team base --defense-team " + opStrategy
        initDist = " --ball-x-min "+str(xMin) + " --ball-x-max "+str(xMax)
        seedParam = " --seed "+str(seed)
        framesParam = " --frames-per-trial "+ str(limitFrames)
              
        

        #Including the name of the executable, default parameters, and the port in the command
        serverCommand = self.serverPath + "HFO --fullstate --offense-on-ball 12 --no-logging --headless " + \
             "--port " +str(self.serverPort)
                         
        #Joining all the commands
        serverCommand += framesParam + agentsParam + opponentsParam + opStrategy + initDist + seedParam + " --verbose >> testlog.log"
        print(serverCommand)
        
        #Starting the server
        self.serverProcess = subprocess.Popen(serverCommand, shell=True)
        time.sleep(2)

        self.clientProcess = []
        for i in range(numberFriends):
            #After starting server, starts friends subprocess
            friendCommand = "python domain/mock_agent.py -p " + str(self.serverPort) + " -o " + str(numberOpponents) + " -f " +str(numberFriends)
            print(friendCommand)
            self.clientProcess.append(subprocess.Popen(friendCommand, shell=True))

        
        
        