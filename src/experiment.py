# -*- coding: utf-8 -*-
"""
Created on May, 25th, 08:29 2017.

@author: Felipe Leno
Source for running the experiments. All the parameters will be here specified and 
all the relevant sources will be called
"""

import argparse
import sys

import csv
import random
#from domain.environment import GridWorld

#from domain.graphics_gridworld import GraphicsGridworld
import os
#from cmac import CMAC


#from agents.agent import Agent
debugImage=False
  


def get_args():
    """Arguments for the experiment
            --task_path: Path for the file defining the final target task
            --algorithm: Learning algorithm (subclass of Agent)
            --learning_episodes: Maximum number of learning episodes to be executed
            --type_evaluation: Type of evaluation (per episodes or per steps)
            --evaluation_interval: interval of episodes for evaluation (episodes or steps)
            --evaluation_duration: Number of evaluation episodes
            --seed: Seed for random procedures
            --log_folder: output folder
            --source_folder: folder with source tasks
            --temp_folder: folder to be possibly used by the algorithm
            --init_trials: initial trial
            --end_trials: final trial
            --curriculum_alg: Algorithm for Curriculum generation
            --termination: Class for termination Condition
            --domain: Class indicating the domain
            
    
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--task_path', default='./tasks/')
    parser.add_argument('-a','--algorithm',  default='Dummy') 
    parser.add_argument('-e','--learning_time',type=int, default=4000)
    parser.add_argument('-te','--type_evaluation',choices=['episode','steps'], default='episode')
    parser.add_argument('-i','--evaluation_interval',type=int, default=100)
    parser.add_argument('-d','--evaluation_duration',type=int, default=10)
    parser.add_argument('-s','--seed',type=int, default=12345)
    parser.add_argument('-l','--log_folder',default='./log/')
    parser.add_argument('-sf','--source_folder',default='./tasks/')
    parser.add_argument('-tf','--temp_folder',default='./temp/')
    parser.add_argument('-it','--init_trials',type=int, default=1)
    parser.add_argument('-et','--end_trials',type=int, default=10)
    parser.add_argument('-ca','--curriculum_alg',default='NoneCurriculum')
    parser.add_argument('-ter','--termination',default="Termination10Episodes")
    parser.add_argument('-do','--domain',choices=['GridWorld','HFODomain'],default="HFODomain")
     

    return parser.parse_args()

def keep_training(task,target_task,curriculum,episodes,steps,totalEpisodes,totalSteps,parameter,termination):
    """
        Given the Curriculum, number of episodes, total number of steps, and parameters,
        defines if the agent still needs to train
    """
    isTarget = task==target_task
    
    #If in the target task, compares the total number of steps, else, calls the termination condition
    if isTarget:
         current = totalEpisodes if parameter.type_evaluation == 'episode' else totalSteps
         keepTraining = current <= parameter.learning_time
    else:
        keepTraining = termination.keep_training(task,target_task,curriculum,episodes,steps,totalEpisodes,totalSteps,parameter)
   
    
    
    return keepTraining
        
def evaluate_now(episodes,totalSteps,parameter,lastEpisodeFinished): 
    """
        Defines if the evaluation should be carried out now
    """
    
    
    if parameter.type_evaluation == 'episode':
        evaluate = episodes  % parameter.evaluation_interval == 0 and lastEpisodeFinished
    else:
        evaluate = totalSteps % parameter.evaluation_interval == 0 
   
    return evaluate
    
    
def build_objects():
    """Builds the objects specified in the argument and returns them in the following order:
        Agent, CurriculumAlg    
            
    """
     
    parameter = get_args()
    
    agentName = getattr(parameter,"algorithm")
    print ("Algorithm: "+agentName)
    try:
            AgentClass = getattr(
               __import__('agents.' + (agentName).lower(),
                          fromlist=[agentName]),
                          agentName)
    except ImportError as error:
            print (error)
            sys.stderr.write("ERROR: missing python module: " +agentName + "\n")
            sys.exit(1)
        
    AGENT = AgentClass(seed=parameter.seed)
 
    #ok AGENT
        
    

    curriculumName = getattr(parameter,"curriculum_alg")
    print( "Curriculum: "+curriculumName)
    try:
            CurriculumClass = getattr(
               __import__('curriculum.' + (curriculumName).lower(),
                          fromlist=[curriculumName]),
                          curriculumName)
    except ImportError as error:
            print( error)
            sys.stderr.write("ERROR: missing python module: " +curriculumName + "\n")
            sys.exit(1)
        
    CURRICULUM = CurriculumClass(seed=parameter.seed,agent = AGENT)
    
    
    terminationName = getattr(parameter,"termination")
    print ("Termination: "+terminationName)
    try:
            TerminationClass = getattr(
               __import__( (terminationName).lower(),
                          fromlist=[terminationName]),
                          terminationName)
    except ImportError as error:
            print( error)
            sys.stderr.write("ERROR: missing python module: " +terminationName + "\n")
            sys.exit(1)
        
    TERMINATION = TerminationClass()
    
    domainName = getattr(parameter,"domain")
    print ("Domain: "+domainName)
    try:
            DomainClass = getattr(
               __import__('domain.' +  (domainName).lower(),
                          fromlist=[domainName]),
                          domainName)
    except ImportError as error:
            print (error)
            sys.stderr.write("ERROR: missing python module: " +domainName + "\n")
            sys.exit(1)
        
    DOMAIN = DomainClass()
    
    return AGENT,CURRICULUM,TERMINATION,DOMAIN
    

def main():
    parameter = get_args()
    print (parameter)
   
    #Folder for temp files
    workFolder = parameter.temp_folder + parameter.algorithm + '/'
    #Full path for task path
    parameter.task_path = parameter.task_path + parameter.domain + "/target.task" 
    #Full path for source tasks
    parameter.source_folder = parameter.source_folder + parameter.domain + "/source/"
    
    

    
    for trial in range(parameter.init_trials,parameter.end_trials+1):
        #Folder for results
        logFolder = parameter.log_folder + parameter.domain + '/'+ parameter.algorithm+"-"+parameter.curriculum_alg
        if not os.path.exists(logFolder):
                os.makedirs(logFolder)
        logFolder = logFolder + "/_0_"+str(trial)+"_AGENT_1_RESULTS"
        
        #Output Files
        eval_csv_file = open(logFolder + "_eval", "w")
        eval_csv_writer = csv.writer(eval_csv_file)
        eval_csv_writer.writerow((parameter.type_evaluation,"steps_completed","reward"))
        eval_csv_file.flush()
        
        print('***** %s: Start Trial' % str(trial))            
        random.seed(parameter.seed+trial)
        agent,curriculum,termination,domain = build_objects()
        
        #links the curriculum algorithm with the learning agent
        #curriculum.set_agent(agent)
        
        
        #Load target Task
        
        environment_target,target_task = domain.build_environment(taskFile=parameter.task_path,limitSteps=200,taskName = 'target')
        
        #Generate Curriculum for target task
        curriculum.generate_curriculum(target_task, parameter.source_folder,workFolder)
        
        #print "--------------- Curriculum---------------------"
        curriculum.print_result()
  
        totalEpisodes = 0 
        totalSteps = 0
        #While there is still tasks to be learned
        while not curriculum.empty_curriculum():
            task = curriculum.draw_task()
            termination.init_task()
            #Initiate task
            environment = domain.build_environment_from_task(task=task,limitSteps=200)
            #environment = environment_target
            environment.start_episode()
            if debugImage:
                    g = GraphicsGridworld(environment)
            
            episodes = 0
            steps = 0
            terminal = False
            lastEpisodeFinished = True
            
            #Verifies termination condition
            while keep_training(task,target_task,curriculum,episodes,steps,totalEpisodes,totalSteps,parameter,termination):
                #Check if it is time to policy evaluation and the agent is training in the target task
                if task==target_task and evaluate_now(totalEpisodes,totalSteps,parameter,lastEpisodeFinished):
#--------------------------------------- Policy Evaluation---------------------------------------------
                    agent.set_exploring(False)
                    agent.connect_env(environment_target)
                    stepsToFinish = 0
                    #Executes the number of testing episodes specified in the parameter
                    sumR = 0
                    numGoals = 0
                    for eval_episode in range(1,parameter.evaluation_duration+1):
                        curGamma = 1.0
                        eval_step = 0
                        
                        environment_target.start_episode()

                        terminal_target= False
                                                
                        while not terminal_target:
                            eval_step += 1
                            state = environment_target.get_state()
                            environment_target.act(agent.select_action(state))
                            
                            #Process state transition
                            statePrime,action,reward = environment_target.step()        
                            #print(environment_target.lastStatus)
                            sumR += reward * curGamma
                            curGamma = curGamma * agent.gamma      
                            
                            if reward==1.0:
                                numGoals += 1
                            
                            terminal_target = environment_target.is_terminal_state()
                        stepsToFinish += eval_step
                        
                    stepsToFinish = float(stepsToFinish) / parameter.evaluation_duration
                    sumR = float(sumR) / parameter.evaluation_duration
                                         
                                         
                    #time = totalEpisodes if parameter.type_evaluation == 'episode' else totalSteps
                    time = totalEpisodes if parameter.type_evaluation == 'episode' else totalSteps
                    numGoals = float(numGoals) / parameter.evaluation_duration
                    eval_csv_writer.writerow((time,"{:.2f}".format(stepsToFinish),"{:.15f}".format(sumR),"{:.2f}".format(numGoals)))
                    eval_csv_file.flush()
                    agent.set_exploring(True) 
                    
                    print("*******Eval OK: EP:"+str(episodes)+" Steps:"+str(totalSteps)+" - Duration: "+str(stepsToFinish))
#-----------------------------------End Policy Evaluation---------------------------------------------
                #One larning step is performed
                totalSteps += 1
                steps += 1
                agent.connect_env(environment)
                
                state = environment.get_state()
                environment.act(agent.select_action(state))
                #Process state transition
                statePrime,action,reward = environment.step()   
                if debugImage:
                    g.update_state()
                agent.observe_reward(state,action,statePrime,reward)
                termination.observe_step(state,action,statePrime,reward)
                
                terminal = environment.is_terminal_state()
                
                #If the agent reached a terminal state, initiates the new episode
                if terminal:
                    totalEpisodes += 1
                    episodes += 1
                    environment.start_episode()
                    agent.finish_episode()
                    termination.finish_episode()
                    lastEpisodeFinished = True
                else:
                    lastEpisodeFinished = False
            agent.finish_learning()
            if debugImage:
                        g.close()
                
            environment.finish_learning()    
        #Close result files
        eval_csv_file.close()
        environment_target.finish_learning()             
    
    
    
    

if __name__ == '__main__':
    main()
