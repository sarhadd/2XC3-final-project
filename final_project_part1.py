import min_heap
import random

import matplotlib.pyplot as plt
import time, math


class DirectedWeightedGraph:

    def __init__(self):
        self.adj = {}
        self.weights = {}

    def are_connected(self, node1, node2):
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]

    def number_of_nodes(self):
        return len(self.adj)


def dijkstra(G, source):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
    Q.decrease_key(source, 0)

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
    return dist


def bellman_ford(G, source):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    nodes = list(G.adj.keys())

    #Initialize distances
    for node in nodes:
        dist[node] = float("inf")
    dist[source] = 0

    #Meat of the algorithm
    for _ in range(G.number_of_nodes()):
        for node in nodes:
            for neighbour in G.adj[node]:
                if dist[neighbour] > dist[node] + G.w(node, neighbour):
                    dist[neighbour] = dist[node] + G.w(node, neighbour)
                    pred[neighbour] = node
    return dist


def total_dist(dist):
    total = 0
    for key in dist.keys():
        total += dist[key]
    return total

def create_random_complete_graph(n,upper):
    G = DirectedWeightedGraph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i,j,random.randint(1,upper))
    return G


#Assumes G represents its nodes as integers 0,1,...,(n-1)
def mystery(G):
    n = G.number_of_nodes()
    d = init_d(G)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] > d[i][k] + d[k][j]: 
                    d[i][j] = d[i][k] + d[k][j]
    return d

def init_d(G):
    n = G.number_of_nodes()
    d = [[float("inf") for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if G.are_connected(i, j):
                d[i][j] = G.w(i, j)
        d[i][i] = 0
    return d

# Sparse graph generator
def create_random_graph(n, p, upper):
    G = DirectedWeightedGraph()
    for i in range(n):
        G.add_node(i)

    for i in range(n):
        for j in range(n):
            if i != j and random.random() < p:
                G.add_edge(i, j, random.randint(1, upper))

    return G

# _____________________________________________________________________
# Approximate Algorithims

def dijkstra_approx(G, source, k):
    dist = {} #Distance dictionary
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    relax_count = {} #Count of times each node have been relaxed
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
        relax_count[node] = 0

    Q.decrease_key(source, 0)
    dist[source] = 0
    
    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key

        for neighbour in G.adj[current_node]:
            if relax_count[neighbour] >= k:
                continue

            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                relax_count[neighbour] += 1
                pred[neighbour] = current_node
    return dist, relax_count


def bellman_ford_approx(G, source, k):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    relax_count = {} #Count of times each node have been relaxed
    nodes = list(G.adj.keys())

    #Initialize distances
    for node in nodes:
        dist[node] = float("inf")
        relax_count[node] = 0
    dist[source] = 0

    #Meat of the algorithm
    for _ in range(G.number_of_nodes()):
        updated = False
        for node in nodes:
            if dist[node] == float("inf"):
                continue
            
            for neighbour in G.adj[node]:
                if relax_count[neighbour] >= k:
                    continue

                if dist[neighbour] > dist[node] + G.w(node, neighbour):
                    dist[neighbour] = dist[node] + G.w(node, neighbour)
                    relax_count[neighbour] += 1
                    pred[neighbour] = node
                    updated = True
        
        if not updated:
            break

    return dist, relax_count

# --------------- Experiment 1: Relative Error vs Graph Size ---------------

def experiment1(ns, upper, k):
    dij_errors = []
    bf_errors = []

    for n in ns:
        G = create_random_complete_graph(n, upper)
        
        # Compute exact distances
        exact_dij = dijkstra(G, 0)
        exact_bf = bellman_ford(G, 0)

        # Compute Approximate distances
        approx_dij, _ = dijkstra_approx(G, 0, k)
        approx_bf, _ = bellman_ford_approx(G, 0, k)
        
        # Compute relative errors
        dij_error = (total_dist(approx_dij) - total_dist(exact_dij)) / total_dist(exact_dij)
        bf_error = (total_dist(approx_bf) - total_dist(exact_bf)) / total_dist(exact_bf)
        dij_errors.append(dij_error)
        bf_errors.append(bf_error)

    return ns, dij_errors, bf_errors

ns = [50, 100, 150, 200]
upper = 10
k = 5

ns_out, dij_errors, bf_errors = experiment1(ns, upper, k)

# plt.plot(ns_out, dij_errors, label="Dijkstra Approximation")
# plt.plot(ns_out, bf_errors, label="Bellman-Ford Approximation")
# plt.title("Experiment 1: Relative Error vs Graph Size")
# plt.xlabel("n (Number of Nodes)")
# plt.ylabel("Relative Error")
# plt.grid(True)
# plt.legend()
# plt.show()


# --------------- Experiment 2: Relative Error vs Density ---------------

def experiment2(n, ps, upper, k):
    dij_errors = []
    bf_errors = []

    for p in ps:
        G = create_random_graph(n, p, upper)

        # Compute exact distances
        exact_dij = dijkstra(G, 0)
        exact_bf = bellman_ford(G, 0)

        # Compute Approximate distances
        approx_dij, _ = dijkstra_approx(G, 0, k)
        approx_bf, _ = bellman_ford_approx(G, 0, k)

        # Compute relative errors
        dij_error = (total_dist(approx_dij) - total_dist(exact_dij)) / total_dist(exact_dij)
        bf_error = (total_dist(approx_bf) - total_dist(exact_bf)) / total_dist(exact_bf)
        dij_errors.append(dij_error)
        bf_errors.append(bf_error)

    return ps, dij_errors, bf_errors


n = 150
ps = [0.05, 0.1, 0.2, 0.5]
upper = 10
k = 5

ps_out, dij_errors, bf_errors = experiment2(n, ps, upper, k)

# plt.plot(ps_out, dij_errors, label="Dijkstra Approximation")
# plt.plot(ps_out, bf_errors, label="Bellman-Ford Approximation")
# plt.title("Experiment 2: Relative Error vs Density")
# plt.xlabel("Density p")
# plt.ylabel("Relative Error")
# plt.grid(True)
# plt.legend()
# plt.show()


# --------------- Experiment 3: Relative Error vs k ---------------

def experiment3(n, upper, ks):
    dij_errors = []
    bf_errors = []

    G = create_random_complete_graph(n, upper)

    # Compute exact distances
    exact_dij = dijkstra(G, 0)
    exact_bf = bellman_ford(G, 0)

    for k in ks:
        # Compute Approximate distances
        approx_dij, _ = dijkstra_approx(G, 0, k)
        approx_bf, _ = bellman_ford_approx(G, 0, k)

        # Compute relative errors
        dij_error = (total_dist(approx_dij) - total_dist(exact_dij)) / total_dist(exact_dij)
        bf_error = (total_dist(approx_bf) - total_dist(exact_bf)) / total_dist(exact_bf)
        dij_errors.append(dij_error)
        bf_errors.append(bf_error)

    return ks, dij_errors, bf_errors

n = 200
upper = 10
ks = [1, 2, 3, 5, 10, 20]

ks_out, dij_errors, bf_errors = experiment3(n, upper, ks)

# plt.plot(ks_out, dij_errors, label="Dijkstra Approximation")
# plt.plot(ks_out, bf_errors, label="Bellman-Ford Approximation")
# plt.title("Experiment 3: Relative Error vs k capacity")
# plt.xlabel("k (Relaxation Capacity)")
# plt.ylabel("Relative Error")
# plt.grid(True)
# plt.legend()
# plt.show()


# --------------- Experiment 4: Distribution of relax_count ---------------

def experiment4(n, upper, k):
    G = create_random_complete_graph(n, upper)

    # Run approximations while capturing relax_count
    _, relax_dij = dijkstra_approx(G, 0, k)
    _, relax_bf = bellman_ford_approx(G, 0, k)

    return list(relax_dij.values()), list(relax_bf.values())

n = 200
upper = 10
k = 5

relax_dij, relax_bf = experiment4(n, upper, k)

# plt.hist(relax_dij, bins=range(0, k+2), alpha=0.5, label="Dijkstra Approx")
# plt.hist(relax_bf, bins=range(0, k+2), alpha=0.5, label="Bellman-Ford Approx")
# plt.title(f"Experiment 4: Distribution of relax_count (k=5)")
# plt.xlabel("Relax Count")
# plt.ylabel("Number of Vertices")
# plt.xticks(range(0, k+1))
# plt.grid(axis='y')
# plt.legend()
# plt.show()


# --------------- Mystery Algorithm Experiment ---------------
# This is a simple experiment to show that mystery function runs in n^3!

def time_mystery(n_val, upper=10):
    timings = []

    for num in n_val:
        G = create_random_complete_graph(num, upper)

        # How much time taken for that amount of n values, n_vals
        start = time.time()
        mystery(G)
        end = time.time()

        timings.append(end - start)

    return timings

# n-values skipping by 10's
n_vals = [20, 30, 40, 50, 60, 70, 80]
timings = time_mystery(n_vals)

# Converting log scale
log_num = [math.log(num) for num in n_vals]
log_time = [math.log(t + 1e-6) for t in timings] # 1e-6 added to t to avoid possible log(0) computations

plt.plot(log_num, log_time)
plt.title("Log/log Runtime Plot of mystery()")
plt.xlabel("log(n)")
plt.ylabel("log(time)")
plt.grid(True)
plt.show()