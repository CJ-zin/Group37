# data_manager.py
import os, json, random
import pandas as pd
import osmnx as ox
import networkx as nx
from models import User, ResidentialStation, MallStation

DATA_DIR = "./data"
CSV_PATH = os.path.join(DATA_DIR, "wasteless250918.csv")
OSM_PATH = os.path.join(DATA_DIR, "hong-kong-260322.osm")
GRAPH_CACHE = os.path.join(DATA_DIR, "graph_cache.json")
USERS_CACHE = os.path.join(DATA_DIR, "users.json")


def create_station_object(st_dict):
    """Instantiate subclass based on the station's characteristics (Mall or Residential)."""
    if "Plaza" in st_dict["name"] or "Mall" in st_dict["name"] or random.random() > 0.7:
        return MallStation(st_dict["id"], st_dict["name"], st_dict["lat"], st_dict["lng"], st_dict["node"],
                           st_dict["waste_types"])
    else:
        return ResidentialStation(st_dict["id"], st_dict["name"], st_dict["lat"], st_dict["lng"], st_dict["node"],
                                  st_dict["waste_types"])


def initialize_network():
    """Load the map graph either from the preprocessed cache or by parsing the raw OSM file."""
    if os.path.exists(GRAPH_CACHE):
        print("[System] Loading network from cache ...")
        with open(GRAPH_CACHE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data["stations"] = [create_station_object(s) for s in data["stations"]]
            return data

    if not os.path.exists(OSM_PATH):
        raise FileNotFoundError(f"Offline map files not found：{OSM_PATH}。")

    print(f"[System] Parsing local OSM XML (please wait 10–30 minutes)...")
    # Build a graph from the local OSM xml map data
    G = ox.graph_from_xml(OSM_PATH)
    largest_wcc = max(nx.weakly_connected_components(G), key=len)
    G = G.subgraph(largest_wcc).copy()
    print("[System] Mapping recycling stations ...")

    # Associate CSV dataset coordinates with map nodes
    df = pd.read_csv(CSV_PATH).dropna(subset=['lat', 'lgt'])
    lats = df['lat'].astype(float).tolist()
    lngs = df['lgt'].astype(float).tolist()

    try:
        nearest_nodes = ox.distance.nearest_nodes(G, X=lngs, Y=lats)
        df['node'] = nearest_nodes
    except Exception as e:
        print(f"[Warning] Failed to match nodes: {e}")
        df['node'] = None

    stations_info = []
    for _, row in df.iterrows():
        if pd.isna(row['node']): continue
        types = [w.strip() for w in str(row['waste_type']).split(',') if w.strip()]
        stations_info.append({
            "id": str(row['cp_id']),
            "name": row['address_tc'] if pd.notna(row['address_tc']) else row['address_en'],
            "lat": float(row['lat']),
            "lng": float(row['lgt']),
            "node": int(row['node']),
            "waste_types": types
        })

    # Generate custom adjacency list to speed up pathfinding
    adj_list = {}
    for u, v, data in G.edges(data=True):
        if u not in adj_list: adj_list[u] = {}
        if v not in adj_list: adj_list[v] = {}
        length = float(data.get('length', 1.0))
        adj_list[u][v] = length
        adj_list[v][u] = length

    nodes_coord = {node: {"lat": float(data['y']), "lng": float(data['x'])} for node, data in G.nodes(data=True)}

    graph_data = {"adj_list": adj_list, "nodes": nodes_coord, "stations": stations_info}
    print("[System] Saving data to cache...")
    with open(GRAPH_CACHE, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False)

    graph_data["stations"] = [create_station_object(s) for s in graph_data["stations"]]
    return graph_data


def save_users(users_dict):
    """Serialize user memory states to local json persistence."""
    data = {
        uid: {
            "name": u.name,
            "password_hash": u._password_hash,
            "salt": u._salt,
            "points": u.points,
            "history": u._recycling_history.get_all_records()
        } for uid, u in users_dict.items()
    }
    with open(USERS_CACHE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def load_users():
    """Deserialize local json objects to construct User instances."""
    if not os.path.exists(USERS_CACHE): return {}
    with open(USERS_CACHE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    users = {}
    for uid, info in data.items():
        pwd_hash, salt = info.get('password_hash'), info.get('salt')
        if pwd_hash and salt:
            u = User(user_id=uid, name=info['name'], password_hash=pwd_hash, salt=salt)
        else:
            u = User(user_id=uid, name=info['name'], password="DefaultPassword123")
        u._points = info.get('points', 0.0)
        # Restore internal history and undo stacks
        for r in info.get('history', []):
            u._recycling_history.append(r)
            if r.get("points", 0) > 0:
                u._action_stack.push(r)
        users[uid] = u
    return users