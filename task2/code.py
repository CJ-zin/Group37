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