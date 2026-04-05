from final_project_part1 import dijkstra, bellman_ford
from final_project_part2 import a_star
import min_heap
from graph_classes import *


class SPAlgorithm:
    def calc_sp(self, G: Graph, s, d): # self, graph, source, dest
        raise NotImplementedError("Subclasses must implement calc_sp")        

class Dijkstra(SPAlgorithm):
    def calc_sp(self, G: WeightedGraph, s, d):
        pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
        dist = {} #Distance dictionary
        Q = min_heap.MinHeap([])
        nodes = list(G.adj.keys())

        #Initialize priority queue/heap and distances
        for node in nodes:
            Q.insert(min_heap.Element(node, float("inf")))
            dist[node] = float("inf")
        Q.decrease_key(s, 0)

        #Meat of the algorithm
        while not Q.is_empty():
            current_element = Q.extract_min()
            current_node = current_element.value
            dist[current_node] = current_element.key
            for neighbour in G.adj[current_node]:
                if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                    Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                    dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                    pred[neighbour] = current_node
        return dist[d]        



class Bellman_Ford(SPAlgorithm):
    def calc_sp(self, G: WeightedGraph, s, d):
        pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
        dist = {} #Distance dictionary
        nodes = list(G.adj.keys())

        #Initialize distances
        for node in nodes:
            dist[node] = float("inf")
        dist[s] = 0

        #Meat of the algorithm
        for _ in range(G.get_num_of_nodes()):
            for node in nodes:
                for neighbour in G.adj[node]:
                    if dist[neighbour] > dist[node] + G.w(node, neighbour):
                        dist[neighbour] = dist[node] + G.w(node, neighbour)
                        pred[neighbour] = node
        return dist[d]



class A_Star(SPAlgorithm):
    def __init__(self, heuristic):
        self.heuristic = heuristic  # store heuristic dictionary

    def calc_sp(self, G: HeuristicGraph, s, d):
        pred = {} # Predecessor dictionary. Isn't returned, but here for your understanding
        dist = {} # Distance dictionary
        Q = min_heap.MinHeap([]) # empty priority queue
        nodes = list(G.adj.keys()) # get all nodes in the graph 

        #Initialize priority queue/heap and distances
        for node in nodes:
            Q.insert(min_heap.Element(node, float("inf")))
            dist[node] = float("inf")
        Q.decrease_key(s, 0 + self.heuristic[s]) # update the priority in the queue (specifically, decrease it)

        #Meat of the algorithm
        while not Q.is_empty():
            current_element = Q.extract_min()
            current_node = current_element.value
            # subtract heuristic since we want pure distance for deciding to update, heuristic is only to maintain priority queue
            dist[current_node] = current_element.key - self.heuristic[current_node] 

            for neighbour in G.adj[current_node]:
                # if a shorter path is found 
                if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]: 
                    # update priority queue based on (distance + heuristic)
                    Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour) + self.heuristic[neighbour])
                    dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                    pred[neighbour] = current_node

            # done after expanding d (which must have been at top of the priority queue)
            if current_node == d: 
                break

        # trace the shortest path 
        # curr = d
        # shortest_path = [d]
        # while curr != s: 
        #     shortest_path.append(pred[curr])
        #     curr = pred[curr]
        # shortest_path.reverse()

        # return (predecessor dictionary, shortest path the algorithm determines from s to d)
        # return pred, shortest_path
        return dist[d]


