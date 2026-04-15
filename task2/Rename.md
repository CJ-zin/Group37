Self-Study Report: Graph Data Structure and Dijkstra's Shortest Path Algorithm

1. Introduction

In this course, we have covered fundamental data structures such as stacks, queues, linked lists, and binary search trees, as well as classic algorithms including merge sort and bubble sort. To expand our knowledge boundaries, this self-study focuses on an in-depth investigation of the Graph—a non-linear data structure—and Dijkstra's Shortest Path Algorithm. Graphs excel at modeling complex relationships between objects, while Dijkstra's algorithm is a foundational greedy approach for solving shortest path problems in such networks. Both have wide-ranging applications in navigation, social networks, and resource scheduling.
2. Data Structure: Graph

2.1 Abstract Data Type (ADT) Definition

A graph is a mathematical structure G = (V, E) consisting of a set of vertices V and a set of edges E. An edge is a pair of vertices (u, v), signifying a relationship between vertex u and vertex v.

• Directed Graph: Edges have a direction, e.g., u \to v.

• Undirected Graph: Edges have no direction, e.g., (u, v).

• Weighted Graph: Edges are associated with numerical values (weights), which can represent distance, cost, or other metrics.

2.2 Core Operations
Operation Description 
add_vertex(v) Adds a vertex  to the graph. 
add_edge(u, v, w) Adds an edge between vertices  and  with weight . 
get_neighbors(v) Retrieves all vertices adjacent to . 
dfs(v) / bfs(v) Performs a Depth-First Search or Breadth-First Search starting from vertex . 

2.3 Implementation Methods

• Adjacency Matrix: A 2D array matrix[i][j] where matrix[i][j] represents the edge from vertex i to vertex j. It has a space complexity of O(V^2) and is suitable for dense graphs.

• Adjacency List: An array or dictionary where each entry stores the neighbors of a vertex and the corresponding edge weights. It has a space complexity of O(V + E) and is more efficient for sparse graphs.

2.4 Application Scenarios

• Map Navigation: Vertices represent locations, edges represent roads, and weights represent distance or travel time.

• Social Networks: Vertices represent users, edges represent friendships, enabling applications like friend recommendations and influence analysis.

• Circuit Design: Vertices represent electronic components, and edges represent the wires connecting them.
3. Algorithm: Dijkstra's Shortest Path Algorithm

3.1 Algorithm Principle

Dijkstra's algorithm is a greedy algorithm used to find the shortest path from a single source vertex to all other vertices in a non-negative weighted graph.

1. Initialization: Set the distance from the source vertex to itself to 0, and the distance to all other vertices to infinity.

2. Iterative Selection: Select the unprocessed vertex u with the smallest known distance from the source.

3. Relaxation: For each neighbor v of u, update the shortest distance to v:

\text{dist}[v] = \min(\text{dist}[v], \text{dist}[u] + \text{weight}(u, v))

4. Mark as Processed: Mark vertex u as processed and repeat steps 2-3 until all vertices are processed.

3.2 Complexity Analysis

• Time Complexity:

◦ Using linear scan to find the minimum vertex: O(V^2).

◦ Optimized with a priority queue (min-heap): O((V + E)\log V), which is the more efficient implementation.

• Space Complexity: O(V), used for storing the distance array and the priority queue.

3.3 Example Demonstration

Consider the following simple undirected weighted graph. We calculate the shortest path from vertex A to all other vertices:
      2       3
  A ----> B ----> C
  | \     |       |
 1|  \4   |5      |1
  |   \   |       |
  v    v  v       v
  D <---- E <---- F
      2       1
Step Processed Vertices Distance Array (A, B, C, D, E, F) Description 
Initialization {} (0, ∞, ∞, ∞, ∞, ∞) Distance from A to itself is 0. 
1 {A} (0, 2, ∞, 1, 4, ∞) Process A, update distances to B, D, and E. 
2 {A, D} (0, 2, ∞, 1, 4, ∞) D is next closest; no neighbor updates. 
3 {A, D, B} (0, 2, 5, 1, 4, ∞) Process B, update distance to C. 
4 {A, D, B, E} (0, 2, 5, 1, 4, 5) Process E, update distance to F. 
5 {A, D, B, E, C} (0, 2, 5, 1, 4, 5) C is next closest; no neighbor updates. 
6 {A, D, B, E, C, F} (0, 2, 5, 1, 4, 5) Process F; algorithm terminates. 

Final shortest paths:

• A → B: 2

• A → D: 1

• A → E: 4

• A → C: A→B→C (5)

• A → F: A→E→F (5)

3.4 Code Implementation (Python)

import heapq

def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

graph = {
    'A': {'B': 2, 'D': 1, 'E': 4},
    'B': {'A': 2, 'C': 3, 'E': 5},
    'C': {'B': 3, 'F': 1},
    'D': {'A': 1},
    'E': {'A': 4, 'B': 5, 'F': 2},
    'F': {'C': 1, 'E': 2}
}

shortest_paths = dijkstra(graph, 'A')
print("Shortest paths from A:", shortest_paths)

4. Conclusion and Future Work

The graph is a powerful data structure for modeling complex relational networks in the real world, and Dijkstra's algorithm is a cornerstone for solving shortest path problems within these networks. Through this self-study, we have gained a deep understanding of the ADT, implementation methods, and applications of graphs, as well as the greedy strategy, complexity analysis, and code implementation of Dijkstra's algorithm.

Limitations: Dijkstra's algorithm cannot handle graphs with negative-weight edges. In such cases, alternatives like the Bellman-Ford algorithm or the Shortest Path Faster Algorithm (SPFA) can be used. For large-scale graphs, more efficient algorithms like the A* heuristic search can be employed.
Would you like me to also translate the README.md for your hk_recycling_system project, or help you adapt this report for a different topic?