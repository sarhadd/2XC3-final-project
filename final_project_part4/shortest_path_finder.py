from algorithms import *
from graph_classes import *

class ShortestPathFinder:
    def __init__(self):
        self.graph = None
        self.algorithm = None
        
    def calc_short_path(self, source: int, dest: int):
        return self.algorithm.calc_sp(self.graph, source, dest)
    
    def set_graph(self, graph: Graph):
        self.graph = graph

    
    def set_algorithm(self, algorithm: SPAlgorithm):
        self.algorithm = algorithm
