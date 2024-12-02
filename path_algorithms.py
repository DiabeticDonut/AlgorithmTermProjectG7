from collections import defaultdict
import osmnx as ox
import networkx as nx
import time

class PathFinder:
    """
    A class that implements various shortest path algorithms for graph traversal.
    Uses NetworkX library for path computation on geographic networks.
    """

    def __init__(self, graph):
        self.G = graph
        
    def dijkstra_path(self, origin, destination):
        start_time = time.time()
        path = nx.dijkstra_path(self.G, origin, destination, weight='length')
        computation_time = time.time() - start_time
        return path, computation_time
    
    def astar_path(self, origin, destination):
        start_time = time.time()
        path = nx.astar_path(self.G, origin, destination, weight='length')
        computation_time = time.time() - start_time
        return path, computation_time
    
    def bellman_ford_path(self, origin, destination):
        start_time = time.time()
        path = nx.bellman_ford_path(self.G, origin, destination, weight='length')
        computation_time = time.time() - start_time
        return path, computation_time
