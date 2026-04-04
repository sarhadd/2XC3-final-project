from algorithims import SPAlgorithm
from graph_classes import Graph, WeightedGraph, HeuristicGraph

class ShortestPathFinder:
    def __init__(self):
        self.graph = None
        self.algorithim = None
        
    # def calc_short_path(self, source: int, dest: int):
    #     raise NotImplementedError
    # You gotta check out the SP algo
    
    def set_graph(self, graph: Graph):
        self.graph = graph

    
    def set_algorithim(self, algorithim: SPAlgorithm):
        self.algorithim = algorithim
