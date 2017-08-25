#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 14:06:12 2017
Graph structure implementation, modified from:
https://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python

"""

from collections import defaultdict


class Graph(object):
    """ Graph data structure, undirected by default. """


    def __init__(self, connections, directed=False):
        self._graph = defaultdict(set)
        self.inEdges = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)
        

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2 in connections:
            self.add(node1, node2)
            

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """

        self._graph[node1].add(node2)
        self.inEdges[node2].add(node1)


    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.iteritems():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        for n, cxns in self.inEdges.iteritems():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
            del self.inEdges[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """

        return node1 in self._graph and node2 in self._graph[node1]

    def find_path(self, node1, node2, path=[]):
        """ Find any path between node1 and node2 (may not be shortest) """

        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def __str__(self):
        name = ""
        for task in self._graph:
            name += "Task:   "+task.name + "\n"
            for nextT in self._graph[task]:
                name +=  "---- "+nextT.name + "\n"
        return name
    def has_edges(self):
        """Is here any edge?"""
        for k in self._graph.keys():
            if len(self._graph[k])>0:
                return True
        return False
    def out_degree(self,node):
        """Returns inDegree of node"""
        return len(self._graph[node])
    def zero_inDegree_nodes(self):
        """Returns all nodes with zero in-degree"""
        nodes = []
        for k in self._graph.keys():
            if len(self.inEdges[k])==0:
                nodes.append(k)
        return nodes
    def remove_edges_from(self,node):
        """Remove all edges from the node"""
        destin = self._graph[node]
        for node2 in destin:
            self.inEdges[node2].remove(node)
        self._graph[node] = set()
        
    def list_children(self,node):
        return self.inEdges[node]
    
    def all_nodes(self):
        return self._graph.keys()