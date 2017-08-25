#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 09:30:04 2017
Controls the port number for automatic hfo task creation
@author: Felipe Leno
"""
import pickle
import os

portFilePath = "/home/leno/gitProjects/Curriculum_HFO/src/.ports"
initialPort = 12345

def get_free_port():
    """Creates the file .ports that stores all the already used port numbers"""
    
    if not os.path.exists(portFilePath):
        open(portFilePath, 'wb').close()
        
        
    portFile = open(portFilePath, 'rb')
    
    if os.path.getsize(portFilePath) > 0:
        dicPorts = pickle.load(portFile)
    else:
        dicPorts = {}
    portFile.close()
    
    #Seeks until a free port is found
    freePort = initialPort
    while dicPorts.get(freePort,False):
        freePort += 5
    
    dicPorts[freePort] = True
    
    portFile = open(portFilePath, 'wb')
    pickle.dump(dicPorts,portFile,pickle.HIGHEST_PROTOCOL)
    portFile.close()
    return freePort
    
def release_port(port):
    """Releases a previously used port"""
    portFile = open(portFilePath, 'rb')
    dicPorts = pickle.load(portFile)
    portFile.close()
    del dicPorts[port]
    portFile = open(portFilePath, 'wb')
    pickle.dump(dicPorts,portFile,pickle.HIGHEST_PROTOCOL)
    portFile.close()
    
    
    
    
