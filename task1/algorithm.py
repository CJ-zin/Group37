# algorithm.py
from data_structures import MinHeap
import math

def get_nearest_node_to_coords(lat, lng, nodes_coord):
    """Find the nearest graph node to the given latitude and longitude using Euclidean distance."""
    min_dist = float('inf')
    nearest_node = None
    for node_id, coord in nodes_coord.items():
        dist = (coord['lat'] - lat) ** 2 + (coord['lng'] - lng) ** 2
        if dist < min_dist:
            min_dist = dist
            nearest_node = node_id
    return nearest_node

def dijkstra_find_station(start_lat, start_lng, waste_type, graph_data):
    """Use Dijkstra's algorithm to find the nearest recycling station accepting the specified waste type."""
    nodes_coord = graph_data["nodes"]
    adj_list = graph_data["adj_list"]

    # Filter stations to only those that accept the target waste type
    valid_stations = [s for s in graph_data["stations"] if waste_type in s.waste_types]
    if not valid_stations:
        return {"error": f"No recycling stations found accepting: {waste_type}"}

    target_nodes = set(str(s.node) for s in valid_stations)
    start_node = str(get_nearest_node_to_coords(start_lat, start_lng, nodes_coord))

    # Initialize distances and priority queue for Dijkstra's shortest path
    distances = {start_node: 0.0}
    previous_nodes = {start_node: None}
    pq = MinHeap()
    pq.push((0.0, start_node))
    visited = set()

    found_target = None
    min_dist = float('inf')

    while not pq.is_empty():
        current_dist, current_node = pq.pop()

        if current_node in visited: continue
        visited.add(current_node)

        # Check if we reached a valid recycling station node
        if current_node in target_nodes:
            found_target = current_node
            min_dist = current_dist
            break

        if current_node not in adj_list: continue

        # Relax adjacent edges
        for neighbor, weight in adj_list[current_node].items():
            neighbor = str(neighbor)
            distance = current_dist + weight
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                pq.push((distance, neighbor))

    if not found_target: return {"error": "Path blocked or no reachable stations."}

    # Reconstruct the shortest path
    path_coords = []
    curr = found_target
    while curr is not None:
        if curr in nodes_coord:
            path_coords.append([nodes_coord[curr]['lat'], nodes_coord[curr]['lng']])
        curr = previous_nodes[curr]
    path_coords.reverse()

    station_obj = next(s for s in valid_stations if str(s.node) == found_target)

    # Return the route data and station information
    return {
        "station": {
            "id": station_obj.id,
            "name": station_obj.name,
            "lat": station_obj.lat,
            "lng": station_obj.lng,
            "type": station_obj.station_type,
            "multiplier": station_obj.multiplier,
            "queue_len": station_obj.queue.size()
        },
        "distance": round(min_dist, 1),
        "path_coords": path_coords,
        "_station_obj": station_obj
    }