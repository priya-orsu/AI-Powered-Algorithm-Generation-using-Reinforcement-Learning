"""
Comprehensive Algorithmic Knowledge Base & Code Generator
Contains verified, executable Python implementations, pseudocode, working steps,
complexities, advantages, disadvantages, and applications for all major CS algorithms.
"""

from typing import Dict, Any, List, Optional
import re

ALGORITHM_CATALOG: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # 1. GRAPH ALGORITHMS
    # =========================================================================
    "dijkstra": {
        "name": "Dijkstra's Algorithm",
        "category": "Graph Algorithms",
        "time_complexity": {"best": "O((V + E) log V)", "average": "O((V + E) log V)", "worst": "O((V + E) log V)"},
        "space_complexity": "O(V)",
        "python_code": """# Dijkstra's Shortest Path Algorithm
import heapq

def dijkstra(graph, start_node):
    \"\"\"
    Computes shortest path distances from start_node to all reachable vertices.
    Graph representation: { 'A': {'B': 4, 'C': 2}, ... }
    \"\"\"
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    predecessors = {node: None for node in graph}
    
    # Priority queue stores tuples of (distance, node)
    pq = [(0, start_node)]
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        if current_dist > distances[u]:
            continue
            
        for v, weight in graph[u].items():
            new_dist = current_dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                predecessors[v] = u
                heapq.heappush(pq, (new_dist, v))
                
    return distances, predecessors

# Demonstration
sample_graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'C': 1, 'D': 5},
    'C': {'B': 1, 'D': 8, 'E': 10},
    'D': {'E': 2},
    'E': {}
}

start_vertex = 'A'
dists, preds = dijkstra(sample_graph, start_vertex)
print(f"Shortest distances from source '{start_vertex}':")
for node, dist in dists.items():
    print(f"  -> To Node {node}: Distance = {dist}")
""",
        "pseudocode": """Algorithm Dijkstra(Graph G, source s)
Input: Weighted directed/undirected graph G = (V, E) with non-negative edge weights, source s
Output: Distances array dist[] and predecessors array prev[]

Begin
    Initialize dist[v] ← ∞ for all v in V, dist[s] ← 0
    Initialize Min-Priority Queue PQ ← [(0, s)]

    While PQ is not empty do
        (d, u) ← PQ.extract_min()
        If d > dist[u] then Continue

        For each neighbor v in G.adjacent[u] do
            alt ← dist[u] + weight(u, v)
            If alt < dist[v] then
                dist[v] ← alt
                prev[v] ← u
                PQ.insert((alt, v))
            End If
        End For
    End While

    Return (dist, prev)
End""",
        "working_steps": [
            "Start",
            "Initialize all vertex distances to infinity (∞) and set the source vertex distance dist[s] = 0.",
            "Insert source vertex (0, s) into the min-priority queue (min-heap).",
            "Extract the vertex u with the smallest known distance from the priority queue.",
            "For each adjacent outgoing edge (u, v) with weight w, calculate candidate distance alt = dist[u] + w.",
            "If alt < dist[v], relax the edge by updating dist[v] = alt and push (alt, v) to the priority queue.",
            "Repeat steps until the priority queue is empty or all reachable vertices are finalized.",
            "Return the finalized shortest path distances and predecessor paths.",
            "Stop"
        ],
        "advantages": [
            "Guarantees optimal shortest paths for all non-negative weighted graphs.",
            "Highly efficient with binary min-heap: O((V + E) log V).",
            "Widely utilized standard for GPS routing and OSPF network protocol."
        ],
        "disadvantages": [
            "Fails to produce correct results on graphs containing negative edge weights.",
            "Requires non-negative edges; use Bellman-Ford if negative weights exist."
        ],
        "applications": ["Google Maps / GPS navigation", "OSPF internet routing protocol", "Robotics path planning"]
    },

    "bellman_ford": {
        "name": "Bellman-Ford Algorithm",
        "category": "Graph Algorithms",
        "time_complexity": {"best": "O(E)", "average": "O(V * E)", "worst": "O(V * E)"},
        "space_complexity": "O(V)",
        "python_code": """# Bellman-Ford Single Source Shortest Path Algorithm
def bellman_ford(vertices, edges, source):
    \"\"\"
    Computes shortest paths from source to all vertices and detects negative weight cycles.
    edges = [ (u, v, weight), ... ]
    \"\"\"
    dist = {v: float('inf') for v in vertices}
    dist[source] = 0
    
    # Relax all edges |V| - 1 times
    for _ in range(len(vertices) - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                
    # Check for negative-weight cycles (Vth relaxation)
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            raise ValueError("Graph contains a negative-weight cycle!")
            
    return dist

# Demonstration
nodes = ['S', 'A', 'B', 'C', 'D', 'E']
graph_edges = [
    ('S', 'A', 10), ('S', 'E', 8),
    ('A', 'C', 2),
    ('B', 'A', 1),
    ('C', 'B', -2),
    ('D', 'C', -1), ('D', 'A', -4),
    ('E', 'D', 1)
]

source_node = 'S'
shortest_paths = bellman_ford(nodes, graph_edges, source_node)
print(f"Bellman-Ford Shortest Paths from Source '{source_node}':")
for node, d in shortest_paths.items():
    print(f"  Distance to {node}: {d}")
""",
        "pseudocode": """Algorithm BellmanFord(Graph G, source s)
Input: Graph G = (V, E), edge weights w, source vertex s
Output: Distances array dist[] or NegativeCycleException

Begin
    Initialize dist[v] ← ∞ for all v in V, dist[s] ← 0

    // Relax all edges |V| - 1 times
    For i ← 1 to |V| - 1 do
        For each edge (u, v) in E with weight w do
            If dist[u] + w < dist[v] then
                dist[v] ← dist[u] + w
            End If
        End For
    End For

    // Detect negative weight cycle
    For each edge (u, v) in E with weight w do
        If dist[u] + w < dist[v] then
            Throw NegativeCycleException
        End If
    End For

    Return dist
End""",
        "working_steps": [
            "Start",
            "Initialize all distances to infinity, setting source vertex distance to 0.",
            "Iterate |V| - 1 times across all edges (u, v) with weight w.",
            "Relax edges: if dist[u] + w < dist[v], update dist[v] = dist[u] + w.",
            "Perform a final pass over all edges to detect negative weight cycles.",
            "If any distance can still be reduced, report negative cycle error.",
            "Return computed shortest path distances.",
            "Stop"
        ],
        "advantages": [
            "Handles graphs with negative edge weights correctly.",
            "Detects and flags negative-weight cycles."
        ],
        "disadvantages": [
            "Slower than Dijkstra: O(V * E) vs O((V + E) log V)."
        ],
        "applications": ["Routing Information Protocol (RIP)", "Financial currency arbitrage detection"]
    },

    "floyd_warshall": {
        "name": "Floyd-Warshall Algorithm",
        "category": "Graph Algorithms",
        "time_complexity": {"best": "O(V^3)", "average": "O(V^3)", "worst": "O(V^3)"},
        "space_complexity": "O(V^2)",
        "python_code": """# Floyd-Warshall All-Pairs Shortest Path Algorithm
def floyd_warshall(graph_matrix):
    \"\"\"
    Computes all-pairs shortest paths using dynamic programming matrix relaxation.
    \"\"\"
    num_nodes = len(graph_matrix)
    # Deep copy distance matrix
    dist = [row[:] for row in graph_matrix]
    
    # Dynamic Programming: Intermediate vertex k
    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    
    return dist

# Demonstration
INF = float('inf')
adjacency_matrix = [
    [0, 3, INF, 7],
    [8, 0, 2, INF],
    [5, INF, 0, 1],
    [2, INF, INF, 0]
]

all_pairs_dist = floyd_warshall(adjacency_matrix)
print("Floyd-Warshall All-Pairs Shortest Distance Matrix:")
for row in all_pairs_dist:
    print(" ", row)
""",
        "pseudocode": """Algorithm FloydWarshall(WeightMatrix W, n)
Input: n x n adjacency weight matrix W
Output: n x n all-pairs shortest distance matrix D

Begin
    D ← Copy(W)

    For k ← 0 to n - 1 do
        For i ← 0 to n - 1 do
            For j ← 0 to n - 1 do
                If D[i][k] + D[k][j] < D[i][j] then
                    D[i][j] ← D[i][k] + D[k][j]
                End If
            End For
        End For
    End For

    Return D
End""",
        "working_steps": [
            "Start",
            "Initialize distance matrix D with direct edge weights and 0 on the diagonal.",
            "Loop intermediate pivot vertex k from 0 to V - 1.",
            "Loop source vertex i from 0 to V - 1 and destination vertex j from 0 to V - 1.",
            "Update D[i][j] = min(D[i][j], D[i][k] + D[k][j]).",
            "Return the all-pairs shortest path matrix.",
            "Stop"
        ],
        "advantages": [
            "Computes shortest paths between all pairs of nodes in a single unified matrix pass.",
            "Extremely simple 3-nested-loop implementation."
        ],
        "disadvantages": [
            "Cubic time complexity O(V^3), making it infeasible for graphs with thousands of nodes."
        ],
        "applications": ["Transitive closure computation", "Network diameter calculation", "Flight path matrix pricing"]
    },

    "a_star": {
        "name": "A* Search Algorithm",
        "category": "Graph & Heuristic Search",
        "time_complexity": {"best": "O(E)", "average": "O(E log V)", "worst": "O(b^d)"},
        "space_complexity": "O(V)",
        "python_code": """# A* Search Heuristic Pathfinding Algorithm
import heapq
import math

def heuristic(a, b):
    # Euclidean distance heuristic: h(n)
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def a_star_search(grid, start, goal):
    \"\"\"
    A* algorithm on a 2D grid with obstacles (0 = open, 1 = obstacle).
    Returns optimal path from start (r, c) to goal (r, c).
    \"\"\"
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, [start]))
    
    g_scores = {start: 0}
    visited = set()
    
    while open_set:
        f_score, g_score, current, path = heapq.heappop(open_set)
        
        if current == goal:
            return path, g_score
            
        if current in visited:
            continue
        visited.add(current)
        
        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                tentative_g = g_score + 1
                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, tentative_g, neighbor, path + [neighbor]))
                    
    return None, float('inf')

# Demonstration
grid_map = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

start_pt = (0, 0)
goal_pt = (4, 4)
path, cost = a_star_search(grid_map, start_pt, goal_pt)
print(f"Optimal A* Path from {start_pt} to {goal_pt}:")
print("Path Coordinates:", path)
print("Total Step Cost:", cost)
""",
        "pseudocode": """Algorithm A_Star(Graph G, start, goal, Heuristic h)
Input: Graph G, start node, goal node, admissible heuristic function h(n)
Output: Optimal path from start to goal

Begin
    Initialize g_score[v] ← ∞ for all v, g_score[start] ← 0
    f_score[start] ← h(start)
    OpenSet ← Min-Priority Queue with (start, f_score[start])

    While OpenSet is not empty do
        current ← OpenSet.extract_min()
        If current = goal then Return ReconstructedPath

        For each neighbor v of current do
            tentative_g ← g_score[current] + weight(current, v)
            If tentative_g < g_score[v] then
                g_score[v] ← tentative_g
                f_score[v] ← tentative_g + h(v)
                OpenSet.insert_or_update(v, f_score[v])
            End If
        End For
    End While

    Return Failure
End""",
        "working_steps": [
            "Start",
            "Set g_score(start) = 0 and calculate f_score(start) = g_score(start) + h(start).",
            "Insert start node into the OpenSet priority queue ordered by f_score.",
            "Extract node with lowest f(n) from OpenSet. If it equals goal, reconstruct and return path.",
            "Explore all valid neighboring nodes and calculate candidate tentative_g = g_score(current) + step_cost.",
            "If tentative_g is lower than recorded g_score(neighbor), update its g_score and f_score = g + h(neighbor).",
            "Push neighbor into OpenSet with its new priority f_score.",
            "Repeat until goal is reached or OpenSet is empty.",
            "Stop"
        ],
        "advantages": [
            "Finds the provably optimal shortest path when heuristic h(n) is admissible and consistent.",
            "Significantly faster than Dijkstra by guiding search directly toward the target.",
            "Widely used in video game AI navigation meshes and autonomous driving."
        ],
        "disadvantages": [
            "High memory consumption because all explored nodes must remain in memory."
        ],
        "applications": ["Game NPC pathfinding", "Autonomous robot navigation", "Geographic mapping engines"]
    },

    "prim": {
        "name": "Prim's Algorithm",
        "category": "Graph Algorithms",
        "time_complexity": {"best": "O(E log V)", "average": "O(E log V)", "worst": "O(E log V)"},
        "space_complexity": "O(V)",
        "python_code": """# Prim's Minimum Spanning Tree (MST) Algorithm
import heapq

def prim_mst(graph, start_vertex):
    \"\"\"
    Computes Minimum Spanning Tree of connected weighted graph using Prim's algorithm.
    Graph representation: { 'A': [('B', 2), ('C', 3)], ... }
    \"\"\"
    visited = set()
    mst_edges = []
    total_cost = 0
    
    pq = [(0, None, start_vertex)]
    
    while pq and len(visited) < len(graph):
        weight, u, v = heapq.heappop(pq)
        
        if v in visited:
            continue
            
        visited.add(v)
        if u is not None:
            mst_edges.append((u, v, weight))
            total_cost += weight
            
        for neighbor, edge_weight in graph.get(v, []):
            if neighbor not in visited:
                heapq.heappush(pq, (edge_weight, v, neighbor))
                
    return mst_edges, total_cost

# Demonstration
graph_data = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2)],
    'E': [('C', 10), ('D', 2)]
}

mst, cost = prim_mst(graph_data, 'A')
print("Prim's Minimum Spanning Tree Edges:")
for u, v, w in mst:
    print(f"  Edge ({u} - {v}) with weight {w}")
print(f"Total Minimum Spanning Tree Weight: {cost}")
""",
        "pseudocode": """Algorithm Prim_MST(Graph G, start_vertex s)
Input: Connected weighted undirected graph G = (V, E), start vertex s
Output: Minimum Spanning Tree (MST) edge set

Begin
    Initialize visited ← Empty Set, MST ← Empty List
    Initialize Min-Heap PQ ← [(0, null, s)]

    While PQ is not empty and |visited| < |V| do
        (weight, u, v) ← PQ.extract_min()

        If v is not in visited then
            visited.add(v)
            If u is not null then MST.append((u, v, weight))

            For each (neighbor, w) in G.adj[v] do
                If neighbor not in visited then PQ.insert((w, v, neighbor))
            End For
        End If
    End While

    Return MST
End""",
        "working_steps": [
            "Start",
            "Select an arbitrary starting vertex and add its incident edges to a min-priority queue.",
            "Mark the starting vertex as visited in the MST tree set.",
            "Extract the edge with the minimum weight from the priority queue connecting visited to unvisited vertices.",
            "If destination vertex is already visited, discard to prevent cycles.",
            "Otherwise, add the edge to MST and mark the destination vertex as visited.",
            "Add all outgoing edges from the newly visited vertex to the priority queue.",
            "Repeat until all vertices in the graph are visited.",
            "Stop"
        ],
        "advantages": [
            "Faster than Kruskal's algorithm on dense graphs with many edges (E ≈ V^2).",
            "Constructs connected tree incrementally without maintaining separate disjoint sets."
        ],
        "disadvantages": [
            "Requires connected graph; for disconnected graphs, runs only on one component."
        ],
        "applications": ["Fiber optic & telecommunication cable layout", "Power grid infrastructure design"]
    },

    "kruskal": {
        "name": "Kruskal's Algorithm",
        "category": "Graph Algorithms",
        "time_complexity": {"best": "O(E log E)", "average": "O(E log E)", "worst": "O(E log E)"},
        "space_complexity": "O(V + E)",
        "python_code": """# Kruskal's Minimum Spanning Tree (MST) with Disjoint Set Union (DSU)
class DisjointSet:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}
        
    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])  # Path compression
        return self.parent[item]
        
    def union(self, u, v):
        root_u, root_v = self.find(u), self.find(v)
        if root_u == root_v:
            return False
        # Union by rank
        if self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        elif self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1
        return True

def kruskal_mst(vertices, edges):
    \"\"\"
    Computes MST by sorting edges and joining forest components via DSU.
    edges = [ (u, v, weight), ... ]
    \"\"\"
    sorted_edges = sorted(edges, key=lambda x: x[2])
    dsu = DisjointSet(vertices)
    mst = []
    total_weight = 0
    
    for u, v, weight in sorted_edges:
        if dsu.union(u, v):
            mst.append((u, v, weight))
            total_weight += weight
            if len(mst) == len(vertices) - 1:
                break
                
    return mst, total_weight

# Demonstration
nodes = ['A', 'B', 'C', 'D', 'E']
edge_list = [
    ('A', 'B', 4), ('A', 'C', 2),
    ('B', 'C', 1), ('B', 'D', 5),
    ('C', 'D', 8), ('C', 'E', 10),
    ('D', 'E', 2)
]

mst_result, total_cost = kruskal_mst(nodes, edge_list)
print("Kruskal's MST Edges:")
for u, v, w in mst_result:
    print(f"  ({u} - {v}) [Weight: {w}]")
print("Total MST Weight:", total_cost)
""",
        "pseudocode": """Algorithm Kruskal_MST(Vertices V, Edges E)
Input: Vertex set V, weighted edge list E
Output: Minimum Spanning Tree edge list MST

Begin
    Sort edges E in non-decreasing order of weight
    Initialize DisjointSet DSU(V)
    Initialize MST ← Empty List

    For each edge (u, v, weight) in sorted E do
        If DSU.find(u) ≠ DSU.find(v) then
            DSU.union(u, v)
            MST.append((u, v, weight))
            If |MST| = |V| - 1 then Break
        End If
    End For

    Return MST
End""",
        "working_steps": [
            "Start",
            "Sort all edges in non-decreasing order of their weights.",
            "Initialize Disjoint Set Union (DSU) structure with each vertex in its own independent set.",
            "Iterate through sorted edges: check if endpoints belong to different sets using DSU Find.",
            "If in different sets, union the two sets and add the edge to the MST.",
            "If in same set, discard edge to prevent forming cycles.",
            "Stop when MST contains exactly |V| - 1 edges.",
            "Stop"
        ],
        "advantages": [
            "Optimal performance on sparse graphs (E ≈ V).",
            "Works naturally on disconnected components to produce Minimum Spanning Forests."
        ],
        "disadvantages": [
            "Requires sorting all edges initially: O(E log E)."
        ],
        "applications": ["LAN network wiring", "Approximation algorithms for TSP", "Circuit design routing"]
    },

    "topological_sort": {
        "name": "Topological Sort",
        "category": "Graph Algorithms",
        "time_complexity": {"best": "O(V + E)", "average": "O(V + E)", "worst": "O(V + E)"},
        "space_complexity": "O(V)",
        "python_code": """# Topological Sort (Kahn's BFS In-Degree Algorithm)
from collections import deque, defaultdict

def topological_sort(vertices, edges):
    \"\"\"
    Computes linear topological ordering of Directed Acyclic Graph (DAG).
    edges = [ (u, v), ... ] meaning directed edge u -> v (u before v).
    \"\"\"
    in_degree = {v: 0 for v in vertices}
    adj = defaultdict(list)
    
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
        
    # Enqueue all nodes with 0 in-degree (no prerequisites)
    queue = deque([v for v in vertices if in_degree[v] == 0])
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    if len(topo_order) != len(vertices):
        raise ValueError("Graph contains a directed cycle; topological ordering impossible.")
        
    return topo_order

# Demonstration
tasks = ['Design', 'Database', 'Backend', 'Frontend', 'Testing', 'Deployment']
dependencies = [
    ('Design', 'Database'),
    ('Design', 'Frontend'),
    ('Database', 'Backend'),
    ('Backend', 'Testing'),
    ('Frontend', 'Testing'),
    ('Testing', 'Deployment')
]

order = topological_sort(tasks, dependencies)
print("Optimal Project Task Execution Sequence (Topological Order):")
for step, task in enumerate(order, 1):
    print(f"  Step {step}: {task}")
""",
        "pseudocode": """Algorithm Kahn_TopologicalSort(Vertices V, Edges E)
Input: Directed graph G = (V, E)
Output: Linear ordering of vertices or CycleException

Begin
    Compute in-degree for all vertices
    Initialize Queue Q ← all vertices with in_degree = 0
    Initialize Order ← Empty List

    While Q is not empty do
        u ← Q.dequeue()
        Order.append(u)

        For each neighbor v in G.adj[u] do
            in_degree[v] ← in_degree[v] - 1
            If in_degree[v] = 0 then
                Q.enqueue(v)
            End If
        End For
    End While

    If |Order| ≠ |V| then Throw CycleException
    Return Order
End""",
        "working_steps": [
            "Start",
            "Calculate the in-degree (number of incoming directed edges) for every vertex.",
            "Enqueue all vertices with in-degree 0 into a FIFO queue.",
            "Dequeue vertex u, append u to the topological ordering result list.",
            "For each adjacent neighbor v of u, decrement in_degree[v] by 1.",
            "If in_degree[v] reaches 0, enqueue v.",
            "Repeat until queue is empty; check if all vertices were ordered (validating DAG property).",
            "Stop"
        ],
        "advantages": [
            "Linear time complexity O(V + E).",
            "Naturally detects cyclic dependencies in task dependency graphs."
        ],
        "disadvantages": [
            "Only valid on Directed Acyclic Graphs (DAGs)."
        ],
        "applications": ["Package managers & build systems (npm, maven, gradle)", "Task scheduling in workflow DAGs (Airflow, Celery)", "Instruction pipelining in compilers"]
    },

    # =========================================================================
    # 2. DYNAMIC PROGRAMMING
    # =========================================================================
    "kadane": {
        "name": "Kadane's Algorithm",
        "category": "Dynamic Programming",
        "time_complexity": {"best": "O(N)", "average": "O(N)", "worst": "O(N)"},
        "space_complexity": "O(1)",
        "python_code": """# Kadane's Algorithm (Maximum Subarray Sum)
def kadane(nums):
    \"\"\"
    Finds maximum sum of contiguous subarray in linear O(N) time and O(1) space.
    \"\"\"
    if not nums:
        return 0, 0, 0
        
    max_so_far = nums[0]
    current_max = nums[0]
    start = end = s = 0
    
    for i in range(1, len(nums)):
        if nums[i] > current_max + nums[i]:
            current_max = nums[i]
            s = i
        else:
            current_max += nums[i]
            
        if current_max > max_so_far:
            max_so_far = current_max
            start = s
            end = i
            
    return max_so_far, nums[start:end + 1]

# Demonstration
array = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
max_sum, subarray = kadane(array)
print("Input Array:", array)
print("Maximum Contiguous Subarray Sum:", max_sum)
print("Optimal Subarray Elements      :", subarray)
""",
        "pseudocode": """Algorithm Kadane(Array A)
Input: Array A of n numbers
Output: Maximum contiguous subarray sum

Begin
    current_sum ← A[0]
    max_sum ← A[0]

    For i ← 1 to n - 1 do
        current_sum ← max(A[i], current_sum + A[i])
        max_sum ← max(max_sum, current_sum)
    End For

    Return max_sum
End""",
        "working_steps": [
            "Start",
            "Initialize current_sum and max_sum with the first element of the array A[0].",
            "Iterate index i from 1 to n - 1 across the array.",
            "At each step, decide whether to start a new subarray at A[i] or extend the previous subarray: current_sum = max(A[i], current_sum + A[i]).",
            "Update max_sum = max(max_sum, current_sum).",
            "Return max_sum after inspecting all elements.",
            "Stop"
        ],
        "advantages": [
            "Optimal linear runtime O(N) with O(1) space overhead.",
            "Simple single-pass accumulator loop."
        ],
        "disadvantages": [
            "Only applies to contiguous subarrays, not non-contiguous subsequences."
        ],
        "applications": ["Stock price profit window analysis", "Image processing 2D bounding filters", "Genomic sequence motif scanning"]
    },

    "knapsack": {
        "name": "0/1 Knapsack Problem",
        "category": "Dynamic Programming",
        "time_complexity": {"best": "O(N * W)", "average": "O(N * W)", "worst": "O(N * W)"},
        "space_complexity": "O(N * W)",
        "python_code": """# 0/1 Knapsack Dynamic Programming Algorithm
def knapsack(weights, values, capacity):
    \"\"\"
    Solves 0/1 Knapsack problem maximizing total profit under weight capacity.
    \"\"\"
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
                
    # Reconstruct selected item indices
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]
            
    return dp[n][capacity], selected[::-1]

# Demonstration
item_weights = [2, 3, 4, 5]
item_values  = [3, 4, 5, 6]
max_cap = 5

max_val, chosen_items = knapsack(item_weights, item_values, max_cap)
print(f"Item Weights: {item_weights}")
print(f"Item Values : {item_values}")
print(f"Knapsack Capacity: {max_cap}")
print(f"Maximum Total Value: {max_val}")
print(f"Chosen Item Indices: {chosen_items}")
""",
        "pseudocode": """Algorithm Knapsack01(Weights W, Values V, Capacity C)
Input: Weights array W, Values array V of n items, Knapsack Capacity C
Output: Maximum achievable value

Begin
    Initialize DP[0..n][0..C] to 0

    For i ← 1 to n do
        For w ← 1 to C do
            If W[i - 1] <= w then
                DP[i][w] ← max(V[i - 1] + DP[i - 1][w - W[i - 1]], DP[i - 1][w])
            Else
                DP[i][w] ← DP[i - 1][w]
            End If
        End For
    End For

    Return DP[n][C]
End""",
        "working_steps": [
            "Start",
            "Initialize a 2D table DP of size (n + 1) x (C + 1) to 0.",
            "Iterate item i from 1 to n and current capacity w from 1 to C.",
            "If item i weight W[i-1] <= w, compute maximum of including or excluding item: max(V[i-1] + DP[i-1][w-W[i-1]], DP[i-1][w]).",
            "Else item exceeds current capacity, inherit previous state: DP[i][w] = DP[i-1][w].",
            "The entry DP[n][C] contains the optimal max value.",
            "Backtrack through the DP table to determine which items were selected.",
            "Stop"
        ],
        "advantages": [
            "Guarantees exact mathematical global optimum.",
            "Can be optimized to O(W) 1D memory array."
        ],
        "disadvantages": [
            "Pseudo-polynomial time complexity dependent on capacity W."
        ],
        "applications": ["Resource allocation in cloud computing", "Cargo loading and container logistics", "Investment portfolio capital allocation"]
    },

    "coin_change": {
        "name": "Coin Change Algorithm",
        "category": "Dynamic Programming",
        "time_complexity": {"best": "O(N * Amount)", "average": "O(N * Amount)", "worst": "O(N * Amount)"},
        "space_complexity": "O(Amount)",
        "python_code": """# Coin Change (Minimum Coins DP)
def coin_change(coins, amount):
    \"\"\"
    Computes minimum number of coins needed to make up amount.
    Returns -1 if amount cannot be formed.
    \"\"\"
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
            
    return dp[amount] if dp[amount] != float('inf') else -1

# Demonstration
available_coins = [1, 2, 5]
target_amount = 11
min_coins = coin_change(available_coins, target_amount)
print("Available Coins:", available_coins)
print("Target Amount:", target_amount)
print(f"Minimum coins required: {min_coins}")
""",
        "pseudocode": """Algorithm CoinChange(Coins C, Amount A)
Input: Coin denominations C, target amount A
Output: Minimum coins to form A or -1

Begin
    Initialize DP[0..A] to ∞, DP[0] ← 0

    For each coin in C do
        For x ← coin to A do
            DP[x] ← min(DP[x], DP[x - coin] + 1)
        End For
    End For

    If DP[A] = ∞ then Return -1
    Return DP[A]
End""",
        "working_steps": [
            "Start",
            "Initialize 1D array DP of size (amount + 1) with infinity (∞), and set DP[0] = 0.",
            "Iterate through each available coin denomination.",
            "For each sub-amount x from coin to target amount, update DP[x] = min(DP[x], DP[x - coin] + 1).",
            "If DP[amount] remains infinity, return -1 indicating impossible combination.",
            "Otherwise return DP[amount] representing minimal coin count.",
            "Stop"
        ],
        "advantages": [
            "Linear space O(Amount) and robust bottom-up dynamic programming.",
            "Handles non-canonical coin systems where greedy selection fails."
        ],
        "disadvantages": [
            "Runtime scales linearly with target amount A."
        ],
        "applications": ["Automated teller machine (ATM) dispensing", "Currency exchange engines", "Vending machine payment logic"]
    },

    "lis": {
        "name": "Longest Increasing Subsequence (LIS)",
        "category": "Dynamic Programming",
        "time_complexity": {"best": "O(N log N)", "average": "O(N log N)", "worst": "O(N log N)"},
        "space_complexity": "O(N)",
        "python_code": """# Longest Increasing Subsequence (Patience Sorting O(N log N))
import bisect

def longest_increasing_subsequence(nums):
    \"\"\"
    Finds the length and sequence of the Longest Strictly Increasing Subsequence.
    Runs in optimal O(N log N) using binary search patience sorting.
    \"\"\"
    if not nums:
        return 0, []
        
    tails = []
    
    for num in nums:
        idx = bisect.bisect_left(tails, num)
        if idx == len(tails):
            tails.append(num)
        else:
            tails[idx] = num
            
    return len(tails), tails

# Demonstration
sequence = [10, 9, 2, 5, 3, 7, 101, 18]
lis_length, lis_tails = longest_increasing_subsequence(sequence)
print("Input Array:", sequence)
print("Length of Longest Increasing Subsequence:", lis_length)
print("Patience Sorting Minimal Tail Array:", lis_tails)
""",
        "pseudocode": """Algorithm LongestIncreasingSubsequence(Array A)
Input: Array A of N numbers
Output: Length of the longest strictly increasing subsequence

Begin
    Initialize Tails ← Empty List
    
    For each number x in A do
        idx ← BinarySearchInsertPosition(Tails, x)
        If idx = length(Tails) then
            Tails.append(x)
        Else
            Tails[idx] ← x
        End If
    End For

    Return length(Tails)
End""",
        "working_steps": [
            "Start",
            "Initialize an empty dynamic array `tails`.",
            "Iterate through each number `x` in the input array.",
            "Use binary search (`bisect_left`) to locate first index in `tails` with value ≥ `x`.",
            "If `x` is larger than all elements in `tails`, append `x` to increase sequence length.",
            "Otherwise, overwrite `tails[idx] = x` to maintain the minimal tail value for that length.",
            "Return length of `tails` array.",
            "Stop"
        ],
        "advantages": [
            "Optimal asymptotic runtime O(N log N).",
            "Minimal auxiliary space consumption O(N)."
        ],
        "disadvantages": [
            "Reconstructing exact original elements requires predecessor tracking array."
        ],
        "applications": ["DNA sequence alignment", "Version control diff algorithms", "Stock market pattern analysis"]
    },

    "lcs": {
        "name": "Longest Common Subsequence (LCS)",
        "category": "Dynamic Programming",
        "time_complexity": {"best": "O(M * N)", "average": "O(M * N)", "worst": "O(M * N)"},
        "space_complexity": "O(M * N)",
        "python_code": """# Longest Common Subsequence (LCS) Dynamic Programming
def longest_common_subsequence(s1, s2):
    \"\"\"
    Computes length and reconstructed string of Longest Common Subsequence.
    \"\"\"
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    lcs_chars = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs_chars.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
            
    return dp[m][n], "".join(reversed(lcs_chars))

# Demonstration
str_a = "ABCBDAB"
str_b = "BDCABA"
length, lcs_str = longest_common_subsequence(str_a, str_b)
print(f"String A: '{str_a}'")
print(f"String B: '{str_b}'")
print(f"LCS Length: {length}")
print(f"Longest Common Subsequence: '{lcs_str}'")
""",
        "pseudocode": """Algorithm LongestCommonSubsequence(String s1, String s2)
Input: String s1 of length m, String s2 of length n
Output: Length of LCS and reconstructed string

Begin
    Initialize DP[0..m][0..n] to 0

    For i ← 1 to m do
        For j ← 1 to n do
            If s1[i - 1] = s2[j - 1] then
                DP[i][j] ← DP[i - 1][j - 1] + 1
            Else
                DP[i][j] ← max(DP[i - 1][j], DP[i][j - 1])
            End If
        End For
    End For

    Return DP[m][n] and BacktrackLCS(DP, s1, s2)
End""",
        "working_steps": [
            "Start",
            "Initialize a 2D matrix DP of size (m+1) x (n+1) with 0s.",
            "Iterate row i from 1 to m and column j from 1 to n.",
            "If characters s1[i-1] and s2[j-1] match, set DP[i][j] = DP[i-1][j-1] + 1.",
            "If characters mismatch, take max(DP[i-1][j], DP[i][j-1]).",
            "DP[m][n] holds maximum length.",
            "Backtrack to reconstruct the actual sequence.",
            "Stop"
        ],
        "advantages": [
            "Guaranteed globally optimal solution using standard dynamic programming principles."
        ],
        "disadvantages": [
            "Standard implementation requires O(M * N) memory."
        ],
        "applications": ["Git diff file comparison", "Bioinformatics DNA alignment", "Plagiarism detection"]
    },

    # =========================================================================
    # 3. ADVANCED DATA STRUCTURES
    # =========================================================================
    "trie": {
        "name": "Trie (Prefix Tree)",
        "category": "Advanced Data Structures",
        "time_complexity": {"best": "O(L)", "average": "O(L)", "worst": "O(L)"},
        "space_complexity": "O(ALPHABET_SIZE * L * N)",
        "python_code": """# Trie (Prefix Tree) Data Structure Implementation
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

# Demonstration
trie = Trie()
words = ["algo", "algorithm", "algogen", "apple", "application"]
for w in words:
    trie.insert(w)

print("Trie Built with Words:", words)
print("Search 'algorithm' :", trie.search("algorithm"))
print("Search 'algor'     :", trie.search("algor"))
print("Starts with 'algo' :", trie.starts_with("algo"))
print("Starts with 'app'  :", trie.starts_with("app"))
print("Starts with 'zoo'  :", trie.starts_with("zoo"))
""",
        "pseudocode": """Class TrieNode
    children: Map<char, TrieNode>
    is_end: boolean

Algorithm TrieInsert(root, word)
    current ← root
    For each char in word do
        If char not in current.children then
            current.children[char] ← New TrieNode()
        End If
        current ← current.children[char]
    End For
    current.is_end ← True

Algorithm TrieSearch(root, word)
    current ← root
    For each char in word do
        If char not in current.children then Return False
        current ← current.children[char]
    End For
    Return current.is_end""",
        "working_steps": [
            "Start",
            "Initialize root TrieNode with empty children dictionary and is_end_of_word = False.",
            "To insert word: iterate through each character token.",
            "If character edge does not exist from current node, instantiate a new TrieNode.",
            "Advance current pointer to child node.",
            "Mark terminal node's is_end_of_word flag as True.",
            "To search/prefix-match: traverse down matching character edges; return False if edge missing.",
            "Stop"
        ],
        "advantages": [
            "Search and insertion run in deterministic O(L) time where L is word length, independent of dictionary size N.",
            "Optimal data structure for autocompletion, spell-checking, and IP prefix routing."
        ],
        "disadvantages": [
            "High memory footprint due to pointer overhead per node."
        ],
        "applications": ["Search engine auto-complete", "Spell checkers & dictionary lookups", "IP routing longest prefix match"]
    },

    "lru_cache": {
        "name": "LRU Cache (Least Recently Used)",
        "category": "Advanced Data Structures",
        "time_complexity": {"best": "O(1)", "average": "O(1)", "worst": "O(1)"},
        "space_complexity": "O(Capacity)",
        "python_code": """# LRU Cache (Least Recently Used) using Doubly Linked List + HashMap
class DNode:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        # Dummy head and tail
        self.head = DNode()
        self.tail = DNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove_node(node)
        self._add_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
            self._add_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                # Evict least recently used (node before tail)
                lru = self.tail.prev
                self._remove_node(lru)
                del self.cache[lru.key]
            new_node = DNode(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)

# Demonstration
lru = LRUCache(2)
lru.put(1, 100)
lru.put(2, 200)
print("Get 1 (Hits cache):", lru.get(1))
lru.put(3, 300) # Evicts key 2
print("Get 2 (Evicted)   :", lru.get(2))
lru.put(4, 400) # Evicts key 1
print("Get 1 (Evicted)   :", lru.get(1))
print("Get 3 (Exists)    :", lru.get(3))
print("Get 4 (Exists)    :", lru.get(4))
""",
        "pseudocode": """Class LRUCache
    capacity: integer
    hash_map: Map<Key, DNode>
    head, tail: DNode

Algorithm LRUGet(key)
    If key not in hash_map then Return -1
    node ← hash_map[key]
    RemoveNode(node)
    AddToHead(node)
    Return node.value

Algorithm LRUPut(key, value)
    If key in hash_map then
        node ← hash_map[key]
        node.value ← value
        RemoveNode(node)
        AddToHead(node)
    Else
        If |hash_map| ≥ capacity then
            lru ← tail.prev
            RemoveNode(lru)
            Delete hash_map[lru.key]
        End If
        new_node ← New DNode(key, value)
        hash_map[key] ← new_node
        AddToHead(new_node)
    End If""",
        "working_steps": [
            "Start",
            "Initialize hash map and doubly linked list with dummy head and tail pointers.",
            "On get(key): check hash map; if present, detach node and re-insert at list head (most recently used); return value.",
            "On put(key, value): if key exists, update value and move to head.",
            "If key is new and cache is full, remove least recently used node located just before tail pointer.",
            "Insert new node into hash map and place at list head.",
            "Stop"
        ],
        "advantages": [
            "Strict O(1) time complexity for both get and put operations.",
            "Maintains constant upper bound on memory usage."
        ],
        "disadvantages": [
            "Requires dual storage (hash table + doubly linked list nodes) with pointer overhead."
        ],
        "applications": ["Operating system virtual memory page replacement", "Redis & Memcached caching engines", "Browser HTTP cache eviction"]
    },

    "huffman": {
        "name": "Huffman Coding Algorithm",
        "category": "Greedy & Compression",
        "time_complexity": {"best": "O(N log K)", "average": "O(N log K)", "worst": "O(N log K)"},
        "space_complexity": "O(K)",
        "python_code": """# Huffman Coding Lossless Data Compression Algorithm
import heapq
from collections import Counter

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    freq_map = Counter(text)
    pq = [HuffmanNode(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(pq)
    
    while len(pq) > 1:
        left = heapq.heappop(pq)
        right = heapq.heappop(pq)
        
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(pq, merged)
        
    return pq[0] if pq else None

def generate_codes(root, current_code="", code_map=None):
    if code_map is None:
        code_map = {}
    if root is not None:
        if root.char is not None:
            code_map[root.char] = current_code or "0"
        generate_codes(root.left, current_code + "0", code_map)
        generate_codes(root.right, current_code + "1", code_map)
    return code_map

def huffman_compress(text):
    root = build_huffman_tree(text)
    codes = generate_codes(root)
    encoded_bits = "".join(codes[ch] for ch in text)
    return encoded_bits, codes

# Demonstration
sample_text = "algorithmic_optimization_engine"
encoded, huffman_codes = huffman_compress(sample_text)
print("Original Text:", sample_text)
print(f"Original Bits (ASCII 8-bit): {len(sample_text) * 8} bits")
print(f"Compressed Huffman Bits   : {len(encoded)} bits")
print(f"Compression Ratio         : {round((1 - len(encoded)/(len(sample_text)*8))*100, 2)}% reduction")
print("Huffman Codebook Table:")
for ch, code in sorted(huffman_codes.items(), key=lambda x: len(x[1])):
    print(f"  '{ch}': {code}")
""",
        "pseudocode": """Algorithm HuffmanCoding(Text T)
Input: String text T of length N
Output: Prefix codebook mapping characters to optimal variable-length bit strings

Begin
    Compute character frequencies Freq[c] for each character in T
    Initialize Min-Priority Queue PQ
    
    For each character c in Freq do
        PQ.insert(HuffmanNode(char = c, freq = Freq[c]))
    End For

    While |PQ| > 1 do
        left ← PQ.extract_min()
        right ← PQ.extract_min()
        parent ← HuffmanNode(freq = left.freq + right.freq)
        parent.left ← left
        parent.right ← right
        PQ.insert(parent)
    End While

    Root ← PQ.extract_min()
    Traverse tree assigning '0' to left and '1' to right branches
    Return CodeMap
End""",
        "working_steps": [
            "Start",
            "Calculate character frequencies across the input text.",
            "Create leaf nodes for each character and insert them into a min-priority queue.",
            "Extract the two nodes with the lowest frequencies from the priority queue.",
            "Create a parent node with sum frequency of both children and attach them as left and right children.",
            "Insert the newly created parent node back into the priority queue.",
            "Repeat extraction and merge until only one root node remains.",
            "Traverse the binary tree from root, appending '0' for left edge and '1' for right edge to assign prefix codes.",
            "Stop"
        ],
        "advantages": [
            "Generates mathematically optimal prefix-free codes for given symbol frequencies.",
            "Lossless compression with no data corruption or degradation.",
            "Foundation of standard compression formats (GZIP, PKZIP, JPEG, MP3)."
        ],
        "disadvantages": [
            "Requires transmitting or storing the Huffman code tree alongside the compressed bitstream."
        ],
        "applications": ["JPEG image compression", "MP3 audio compression", "GZIP / DEFLATE archiving", "Network packet compression"]
    },

    # =========================================================================
    # 4. MACHINE LEARNING & CLUSTERING
    # =========================================================================
    "k_means": {
        "name": "K-Means Clustering Algorithm",
        "category": "Machine Learning & Clustering",
        "time_complexity": {"best": "O(K * N * D)", "average": "O(I * K * N * D)", "worst": "O(I * K * N * D)"},
        "space_complexity": "O(N * D + K * D)",
        "python_code": """# K-Means Unsupervised Clustering Algorithm
import random
import math

def euclidean_distance(p1, p2):
    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))

def k_means(points, k=3, max_iters=20):
    \"\"\"
    Partitions N data points into K clusters minimizing squared Euclidean distances.
    \"\"\"
    centroids = random.sample(points, k)
    
    for iteration in range(max_iters):
        clusters = [[] for _ in range(k)]
        
        for pt in points:
            distances = [euclidean_distance(pt, c) for c in centroids]
            best_cluster = distances.index(min(distances))
            clusters[best_cluster].append(pt)
            
        new_centroids = []
        for cluster in clusters:
            if not cluster:
                new_centroids.append(random.choice(points))
                continue
            dim = len(cluster[0])
            avg_coords = [sum(pt[d] for pt in cluster) / len(cluster) for d in range(dim)]
            new_centroids.append(avg_coords)
            
        if new_centroids == centroids:
            break
        centroids = new_centroids
        
    return centroids, clusters

# Demonstration
sample_points = [
    [1.0, 1.2], [1.5, 1.8], [1.2, 0.8],
    [8.0, 8.5], [8.2, 9.0], [7.8, 8.1],
    [1.1, 8.9], [1.3, 9.2], [0.9, 8.7]
]

k = 3
final_centroids, grouped_clusters = k_means(sample_points, k)
print(f"K-Means Clustering Result for K = {k}:")
for idx, (centroid, cluster) in enumerate(zip(final_centroids, grouped_clusters)):
    print(f"  Cluster {idx + 1} Centroid: ({centroid[0]:.2f}, {centroid[1]:.2f}) -> {len(cluster)} points")
""",
        "pseudocode": """Algorithm KMeans(Points P, integer K, max_iter)
Input: Collection of N d-dimensional points P, number of clusters K
Output: Centroids C[1..K] and cluster assignments

Begin
    Initialize K centroids C[1..K] randomly from P

    For iter ← 1 to max_iter do
        Clear cluster assignments Clusters[1..K]

        For each point p in P do
            c_idx ← argmin_j ||p - C[j]||^2
            Clusters[c_idx].append(p)
        End For

        For j ← 1 to K do
            If |Clusters[j]| > 0 then
                C[j] ← Mean(Clusters[j])
            End If
        End For

        If Centroids converged then Break
    End For

    Return (C, Clusters)
End""",
        "working_steps": [
            "Start",
            "Choose K initial cluster centroids randomly from the dataset or via K-Means++ initialization.",
            "Compute the Euclidean distance between every data point and all K centroids.",
            "Assign each data point to its closest centroid cluster.",
            "Recompute the position of each centroid by calculating the arithmetic mean of all points assigned to that cluster.",
            "Check convergence: if centroids moved less than threshold epsilon, stop.",
            "Otherwise repeat assignment and update phases until max iterations or convergence.",
            "Stop"
        ],
        "advantages": [
            "Fast, computationally lightweight and scales easily to massive datasets.",
            "Simple, intuitive mathematical foundation with linear iteration complexity."
        ],
        "disadvantages": [
            "Requires user to pre-specify the number of clusters K.",
            "Sensitive to initial centroid seeds and susceptible to local minima."
        ],
        "applications": ["Customer market segmentation", "Image color quantization", "Anomaly and fraud detection"]
    }
}

def get_comprehensive_algorithm(algorithm_name: str, category: str = "General") -> Optional[Dict[str, Any]]:
    """Checks if query matches any curated high-fidelity algorithm definition."""
    clean = algorithm_name.lower().strip()
    
    # Exact and keyword matches
    for key, data in ALGORITHM_CATALOG.items():
        if key in clean or clean in key or data["name"].lower() in clean or clean in data["name"].lower():
            return data
            
    # Fuzzy alias checks
    if "dijkstra" in clean:
        return ALGORITHM_CATALOG["dijkstra"]
    if "bellman" in clean:
        return ALGORITHM_CATALOG["bellman_ford"]
    if "floyd" in clean or "warshall" in clean:
        return ALGORITHM_CATALOG["floyd_warshall"]
    if "a*" in clean or "a star" in clean:
        return ALGORITHM_CATALOG["a_star"]
    if "prim" in clean:
        return ALGORITHM_CATALOG["prim"]
    if "kruskal" in clean:
        return ALGORITHM_CATALOG["kruskal"]
    if "topological" in clean or "kahn" in clean:
        return ALGORITHM_CATALOG["topological_sort"]
    if "kadane" in clean or "max subarray" in clean or "maximum subarray" in clean:
        return ALGORITHM_CATALOG["kadane"]
    if "knapsack" in clean:
        return ALGORITHM_CATALOG["knapsack"]
    if "coin change" in clean or "coin_change" in clean:
        return ALGORITHM_CATALOG["coin_change"]
    if "huffman" in clean:
        return ALGORITHM_CATALOG["huffman"]
    if "lis" in clean or "increasing subsequence" in clean:
        return ALGORITHM_CATALOG["lis"]
    if "lcs" in clean or "common subsequence" in clean:
        return ALGORITHM_CATALOG["lcs"]
    if "kmeans" in clean or "k-means" in clean or "k means" in clean:
        return ALGORITHM_CATALOG["k_means"]
    if "trie" in clean:
        return ALGORITHM_CATALOG["trie"]
    if "lru" in clean or "lru cache" in clean or "least recently used" in clean:
        return ALGORITHM_CATALOG["lru_cache"]
        
    return None
