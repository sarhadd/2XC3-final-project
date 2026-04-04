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
        
  
# Computing Euclidean distance between two stations
def distance(lat1,lon1, lat2,lon2 ):
    return math.sqrt((lat1 - lat2 ) ** 2 + (lon1 - lon2)**2)
    

# Building the graph (adjacency list) and storing weights 
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
    
    
# building the heuristic: distance from each node to destination
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

########################        Time Algorithm          ##############################

def time_algorithms(G, s, d):
    h = build_heuristic(d)
    
    # For A*
    start = time.time()
    _,path_a = a_star(G, s,d, h)
    t_a = time.time() - start
    
    # For Dijkstra
    start = time.time()
    dist_d = dijkstra(G, s)
    t_d = time.time() - start
    
    return t_a, t_d, path_a

######################## Runtime Experiment & Line Analysis ##############################

# Map each edge to its subway line (to analyze tranfers in path)
line_map = {}
with open("london_connections.csv", "r") as file:
    reader = csv.DictReader(file)
    
    for row in reader: 
        s1 = int(row["station1"])
        s2 = int(row["station2"])
        line = row["line"]
        
        line_map[(s1,s2)] = line
        line_map[(s2,s1)] = line
        
# Counting ho many times the path chnages subway lines (transfers)
def count_transfers(path):
    lines_used = []
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        lines_used.append(line_map[(u, v)])
    
    transfers = 0
    for i in range(1, len(lines_used)):
        if lines_used[i] != lines_used[i - 1]:
            transfers += 1  
    return transfers

# Running experiments on all station pairs and record runtime and number of transfers
results = []

nodes = list(stations.keys()) 
for s in nodes: 
    for d in nodes:
        if s != d:
            t_a, t_d, path_a = time_algorithms(G,s,d)
            
            transfers = count_transfers(path_a)
            
            results.append({
                "s" : s, 
                "d" : d,
                "t_a": t_a,
                "t_d": t_d,
                "diff": t_d - t_a, # if this is positive then A* is faster 
                "transfers": transfers
            })

# Grouping results based on runtime comparison
a_better = [r for r in results if r["t_a"] < r["t_d"]]
d_better = [r for r in results if r["t_d"] < r["t_a"]]
similar = [r for r in results if abs(r["t_a"] - r["t_d"]) < 1e-5]

# Grouping results based on number of transfers
same_line = [r for r in results if r["transfers"] == 0]
one_transfer = [r for r in results if r["transfers"] == 1]
many_transfers = [r for r in results if r["transfers"] >= 2]

# print("A* better:", len(a_better))
# print("Dijkstra better:", len(d_better))
# print("Similar:", len(similar))

# Computing average rune time for given group of results
def avg_time(data, key): 
    total = 0
    for r in data: 
        total += r[key]
    return total / len(data)

print("\nSame line:")
print("A* :", avg_time(same_line, "t_a"))
print("Dijkstra: ", avg_time(same_line, "t_d"))

print("\nOne transfer:")
print("A* :", avg_time(one_transfer, "t_a"))
print("Dijkstra: ", avg_time(one_transfer, "t_d"))

print("\nMany transfers:")
print("A* :", avg_time(many_transfers, "t_a"))
print("Dijkstra: ", avg_time(many_transfers, "t_d"))




