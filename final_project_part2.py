from final_project_part1 import *

# G = Directed weighted graph 
# s = Source node 
# d = Destination node 
# h = Heuristic function. This is a dictionary which takes in a node (int) and returns a float. 

def a_star(G, s, d, h): 
    pred = {} # Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} # Distance dictionary
    Q = min_heap.MinHeap([]) # empty priority queue
    nodes = list(G.adj.keys()) # get all nodes in the graph 

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
    Q.decrease_key(s, 0 + h[s]) # update the priority in the queue (specifically, decrease it)

    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        # subtract heuristic since we want pure distance for deciding to update, heuristic is only to maintain priority queue
        dist[current_node] = current_element.key - h[current_node] 

        for neighbour in G.adj[current_node]:
            # if a shorter path is found 
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]: 
                # update priority queue based on (distance + heuristic)
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour) + h[neighbour])
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                pred[neighbour] = current_node

        # done after expanding d (which must have been at top of the priority queue)
        if current_node == d: 
            break

    # trace the shortest path 
    curr = d
    shortest_path = [d]
    while curr != s: 
        shortest_path.append(pred[curr])
        curr = pred[curr]
    shortest_path.reverse()

    # return ({predecessor dictionary}, shortest path the algorithm determines from s to d)
    return dist[d], shortest_path

