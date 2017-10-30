"""

Creates an agent with fixed policy:

If goal opening > 0.4 tries to shoot, else passes the ball to a friendly agent (random)
@author: Felipe Leno
"""
import sys, itertools
from hfo import *
import argparse
import random

def get_args():
    """Arguments for the experiment
            --port: Port to server connection
            --seed: Seed for random number generation
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=6000)
    parser.add_argument('-s', '--seed', type=int, default=12345)
    parser.add_argument('-o', '--opponents', type=int, default=2)
    parser.add_argument('-f', '--friends', type=int, default=1)
    return parser.parse_args()

def main():

  argument = get_args()

  # Create the HFO Environment
  hfo = HFOEnvironment()
  # Connect to the server with the specified
  # feature set. See feature sets in hfo.py/hfo.hpp.
  hfo.connectToServer(HIGH_LEVEL_FEATURE_SET,
                      '../../HFO/bin/teams/base/config/formations-dt', argument.port,
                      'localhost', 'base_left', False)
  for episode in itertools.count():
    status = IN_GAME
    while status == IN_GAME:
      # Grab the state features from the environment
      features = hfo.getState()
      #print(features)
      #Has the ball possession?
      if features[5] == 1.0:
          #If OPPONENT_PROXIMITY smaller than 0.3, passes the ball
          #print("GOAL OPENING "+str( features[8] ))
          if argument.opponents > 0 and abs(features[9]) > 0.3:
              hfo.act(DRIBBLE)
              #print("SHOOTING")
          else:
              #Searching for ids of friends
              if argument.opponents > 0:
                  initIndex = 9
              else:
                  initIndex = 8
              initIndex += 3* argument.friends
              ids = []
              for i in range(argument.friends):
                  initIndex += 3
                  ids.append(features[initIndex])
              friendUnum = random.choice(ids)
              hfo.act(PASS,friendUnum)
              #print("PASSING " + str(friendUnum))
      else:
          hfo.act(MOVE)
          #print("MOVING")

      status = hfo.step()

    # Quit if the server goes down
    if status == SERVER_DOWN:
      hfo.act(QUIT)
      exit()

if __name__ == '__main__':
  main()