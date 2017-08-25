#!/usr/bin/env python
# encoding: utf-8

# Before running this program, first Start HFO server:
# $> ./bin/HFO --offense-agents 1

from __future__ import print_function
from threading import Thread
import argparse
import itertools
import random
import os,signal
import subprocess
import time
try:
  import hfo
except ImportError:
  print('Failed to import hfo. To install hfo, in the HFO directory'\
    ' run: \"pip install .\"')
  exit()

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', type=int, default=12345,
                      help="Server port")
  parser.add_argument('--seed', type=int, default=None,
                      help="Python randomization seed; uses python default if 0 or not given")
  parser.add_argument('--record', action='store_true',
                      help="Doing HFO --record")
  parser.add_argument('--rdir', type=str, default='log/',
                      help="Set directory to use if doing HFO --record")
  args=parser.parse_args()
  
  serverCommands = [
     "/home/leno/gitProjects/Curriculum_HFO/HFO/bin/HFO --offense-team helios --fullstate --offense-on-ball 12 --no-logging --headless --port 12345 --frames-per-trial 200 --offense-agents 1 --offense-npcs 2 --defense-npcs 3 --offense-team base --defense-team helios --ball-x-min 0.6 --ball-x-max 0.7999999999999999 --seed 123 --verbose >> tt.log",
     "/home/leno/gitProjects/Curriculum_HFO/HFO/bin/HFO --offense-team helios --fullstate --offense-on-ball 12 --no-logging --headless --port 12350 --frames-per-trial 200 --offense-agents 1 --offense-npcs 2 --defense-npcs 3 --offense-team base --defense-team helios --ball-x-min 0.6 --ball-x-max 0.7999999999999999 --seed 123 --verbose >> tt.log",
     "/home/leno/gitProjects/Curriculum_HFO/HFO/bin/HFO --offense-team helios --fullstate --offense-on-ball 12 --no-logging --headless --port 12355 --frames-per-trial 200 --offense-agents 1 --offense-npcs 2 --defense-npcs 3 --offense-team base --defense-team helios --ball-x-min 0.6 --ball-x-max 0.7999999999999999 --seed 123 --verbose >> tt.log",
     "/home/leno/gitProjects/Curriculum_HFO/HFO/bin/HFO --offense-team helios --fullstate --offense-on-ball 12 --no-logging --headless --port 12360 --frames-per-trial 200 --offense-agents 1 --offense-npcs 2 --defense-npcs 3 --offense-team base --defense-team helios --ball-x-min 0.6 --ball-x-max 0.7999999999999999 --seed 123 --verbose >> tt.log"
   ]
  
  for serverCommand in serverCommands:
      serverProcess = subprocess.Popen(serverCommand, shell=True)
  
      print("NEW Server")
        
      time.sleep(1)
      if args.seed:
          random.seed(args.seed)
      # Create the HFO Environment
      hfo_env = hfo.HFOEnvironment()

      # Connect to the server with the specified
      # feature set. See feature sets in hfo.py/hfo.hpp.
      t = Thread(target=init_connect, args=(hfo_env,args))
      t.start()
      t.join()
      
  
  
      subprocess.call("kill -9 -"+str(serverProcess.pid), shell=True)
      args.port = args.port+5
 

"""  for episode in range(100):
      t1 = Thread(target=run_learning, args=(hfo_env,args,episode))
      t1.start()
      t1.join()
  hfo_env = None
  
  
  terminateThread = {}
  terminateThread['f'] = False
  t = Thread(target=init_server, args=(serverCommand,terminateThread))
  t.start()

  hfo_env2 = hfo.HFOEnvironment()
  t = Thread(target=init_connect, args=(hfo_env2,args))
  t.start()
  t.join()
  for episode in range(100):
      t = Thread(target=run_learning, args=(hfo_env2,args,episode))
      t.start()
      t.join()"""
      

def init_server(serverCommand,terminateThread):
    try:
        serverProcess = subprocess.Popen(serverCommand, shell=True)
        print("OK Server")
        while not terminateThread['f']:
            time.sleep(1)
            print("--------------- " +str(serverProcess.pid)+"--------")
         
        import os,signal
        os.killpg(os.getpgid(serverProcess.pid), signal.SIGTERM) 
    except Exception:
        print( "Except")
        
        
        
def init_connect(hfo_env,args): 
  if args.record:
    hfo_env.connectToServer(hfo.HIGH_LEVEL_FEATURE_SET,
                            '/home/leno/gitProjects/Curriculum_HFO/HFO/bin/teams/base/config/formations-dt', args.port,
                            'localhost', 'base_left', False,
                            record_dir=args.rdir)
  else:
    hfo_env.connectToServer(hfo.HIGH_LEVEL_FEATURE_SET,
                            '/home/leno/gitProjects/Curriculum_HFO/HFO/bin/teams/base/config/formations-dt', args.port,
                            'localhost', 'base_left', False)
    for episode in range(100):
      #t1 = Thread(target=run_learning, args=(hfo_env,args,episode))
      #t1.start()
      #t1.join()
        status = hfo.IN_GAME
        while status == hfo.IN_GAME:
          # Get the vector of state features for the current state
          state = hfo_env.getState()
          # Perform the action
          if state[5] == 1: # State[5] is 1 when the player can kick the ball
            if random.random() < 0.5: # more efficient than random.choice for 2
              hfo_env.act(hfo.SHOOT)
            else:
              hfo_env.act(hfo.DRIBBLE)
          else:
            hfo_env.act(hfo.MOVE)
          # Advance the environment and get the game status
    
          status = hfo_env.step()
    
        # Check the outcome of the episode
        end_status = hfo_env.statusToString(status)
        print("Episode {} ended with {}".format(episode, end_status))
    
        # Quit if the server goes down
        if status == hfo.SERVER_DOWN:
          hfo_env.act(hfo.QUIT)
          print("Server DOWN")
          exit()
def run_learning(hfo_env,args,episode):
    status = hfo.IN_GAME
    while status == hfo.IN_GAME:
      # Get the vector of state features for the current state
      state = hfo_env.getState()
      # Perform the action
      if state[5] == 1: # State[5] is 1 when the player can kick the ball
        if random.random() < 0.5: # more efficient than random.choice for 2
          hfo_env.act(hfo.SHOOT)
        else:
          hfo_env.act(hfo.DRIBBLE)
      else:
        hfo_env.act(hfo.MOVE)
      # Advance the environment and get the game status

      status = hfo_env.step()

    # Check the outcome of the episode
    end_status = hfo_env.statusToString(status)
    print("Episode {} ended with {}".format(episode, end_status))

    # Quit if the server goes down
    if status == hfo.SERVER_DOWN:
      hfo_env.act(hfo.QUIT)
      exit()
    

if __name__ == '__main__':
  main()
