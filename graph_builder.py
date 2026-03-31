import csv
import math
import time
from final_project_part1 import dijkstra
from final_project_part2 import a_star

stations = {}     #creating a dictionary of stations 
with open("london_stations.csv", "r") as file:
    reader = csv.DictReader(file)
    
    for row in reader: 
        stations_id = int(row["id"]) # This gives stations id
        lat = float(row["latitude"]) # The locations of the station (Need them for building the weights)
        lon = float(row["longitude"])
        
        stations[stations_id] = (lat, lon)
        
        
# print(list(stations.items())[:5])
def distance(lat1,lon1, lat2,lon2 ):
    return math.sqrt((lat1 - lat2 ) ** 2 + (lon1 - lon2)**2)
    

# Building the graph (adjacency list)
class Graph:
    def __init__(self, adj, weights):
        self.adj = adj
        self.weights = weights
    def w(self, u, v):
        return self.weights[(u,v)]

graph = {}

for station in stations:
    graph[station] = []
    
weights = {}

# Reading the connections from london_connections.csv file
with open("london_connections.csv", "r") as file: 
    reader = csv.DictReader(file)
    
    for row in reader:
        s1 = int(row["station1"])
        s2 = int(row["station2"])
        
        # Using 1 for now instead of weights 
        lat1, lon1 = stations[s1]
        lat2, lon2 = stations[s2]
        
        w = distance(lat1, lon1, lat2, lon2)
        
        graph[s1].append(s2)
        graph[s2].append(s1)
        

        weights[(s1,s2)] = w
        weights[(s2,s1)] = w

        
G = Graph(graph , weights)
        
#testing:
#print(graph[52])
#print(len(graph))
    
    
# building the heuristic (but how is this will be turn into a guess?? Youtube watch! )
def build_heuristic(destination): 
    h = {}
    lat_d, lon_d = stations[destination]
    
    for node in stations:
        lat, lon = stations[node]
        h[node] = distance(lat,lon, lat_d, lon_d)
        
    return h
    
    

# print(graph[52][:5])   # check weights look reasonable
# h = build_heuristic(100)
# print(h[52])
# print(h[100])

# one test for debugging: 
# s = 52
# d = 100
# h = build_heuristic(d)

# def path_cost(G, path):
#     total = 0
#     for i in range(len(path) - 1):
#         total += G.w(path[i], path[i+1])
#     return total
# pred_a, path_a = a_star(G, s, d, h)
# cost_a = path_cost(G, path_a)
# dist_d = dijkstra(G, s)
# print("A* cost: ", cost_a)
# print("Dijkstra distance to d: ", dist_d[d]) 


