#!/usr/bin/env python
# encoding: utf-8

# Before running this program, first Start HFO server:
# $> ./bin/HFO --offense-agents 1

import itertools
from hfo import *
import random

def main():
  # Create the HFO Environment
  hfo = HFOEnvironment()
  # Connect to the server with the specified
  # feature set. See feature sets in hfo.py/hfo.hpp.
  hfo.connectToServer(HIGH_LEVEL_FEATURE_SET,
                      '/home/leno/gitProjects/Curriculum_HFO/HFO/bin/teams/base/config/formations-dt', 2000,
                      'localhost', 'base_left', False)
  for episode in itertools.count():
    status = IN_GAME
    while status == IN_GAME:
      # Grab the state features from the environment
      features = hfo.getState()
      if features[4] == 1.0:
          action = random.choice(DRIBBLE,SHOOT,PASS)
      else:
          action = MOVE
      if action == PASS:
          hfo.act(action,1)
      else:
         hfo.act(action)   
      # Take an action and get the current game status
      
      # Advance the environment and get the game status
      status = hfo.step()
    # Check the outcome of the episode
    print(('Episode %d ended with %s'%(episode, hfo.statusToString(status))))
    # Quit if the server goes down
    if status == SERVER_DOWN:
      hfo.act(QUIT)
      exit()

if __name__ == '__main__':
  main()
