class Graph:

    def __init__(self):
        self.adj = {}
        self.weights = {}

    # def are_connected(self, node1, node2):
    #     for neighbour in self.adj[node1]:
    #         if neighbour == node2:
    #             return True
    #     return False

    def get_adj_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def w(self, node): 
        return 1 # i assume? 

    # def w(self, node1, node2):
    #     if self.are_connected(node1, node2):
    #         return self.weights[(node1, node2)]

    def get_num_of_nodes(self):
        return len(self.adj)


# references: https://www.w3schools.com/python/python_inheritance.asp 
class WeightedGraph(Graph): 
    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]
        
# references: https://www.geeksforgeeks.org/python/access-modifiers-in-python-public-private-and-protected/ 
class HeuristicGraph(WeightedGraph):         
    def __heuristic(self, h): 
        # create the heuristic??? 
        self.h = h 

    def get_heuristic(self): 
        return self.h