import csv
import math

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
graph = {}

for station in stations:
    graph[station] = []
    
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
        
        graph[s1].append((s2, w))
        graph[s2].append((s1, w))
        
        
        
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
    
    
