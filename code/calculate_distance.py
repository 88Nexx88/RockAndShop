import json
import os.path
import osmnx as ox
import networkx as nx
import pandas as pd
import yaml
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

G_drive, G_walk = ox.load_graphml('drive.graphml'), ox.load_graphml('walk.graphml')

def write_data(filename: str, current_dict: dict, flag: str):
    with open(filename, 'w') as write_file:
        match flag:
            case "json": json.dump(current_dict, write_file, indent=3, ensure_ascii=False)

            case "yaml": yaml.dump(current_dict, write_file, default_flow_style=False)

def tuple_constructor(loader, node): return tuple(loader.construct_sequence(node))

if os.path.exists("cache_walk.yaml") and os.path.exists("cache_drive.yaml"):
    print('try')
    # Зарегистрируем конструктор для тега 'tag:yaml.org,2002:python/tuple'
    yaml.SafeLoader.add_constructor('tag:yaml.org,2002:python/tuple', tuple_constructor)

    with open('cache_walk.yaml', 'r') as yaml_file: nearest_nodes_cache_walk = yaml.safe_load(yaml_file)

    with open('cache_drive.yaml', 'r') as yaml_file: nearest_nodes_cache_drive = yaml.safe_load(yaml_file)

else:
    print('except')
    nearest_nodes_cache_drive, nearest_nodes_cache_walk = dict(), dict()



def calculate_distance(lat1, lon1, lat2, lon2, flag: str) -> int:
    global nearest_nodes_cache_drive, nearest_nodes_cache_walk
    match flag:
        case "drive":
            if (lat1, lon1) not in nearest_nodes_cache_drive: nearest_nodes_cache_drive[(lat1, lon1)] = ox.distance.nearest_nodes(G_drive, lon1, lat1)

            if (lat2, lon2) not in nearest_nodes_cache_drive: nearest_nodes_cache_drive[(lat2, lon2)] = ox.distance.nearest_nodes(G_drive, lon2, lat2)

            orig_node, dest_node = nearest_nodes_cache_drive[(lat1, lon1)], nearest_nodes_cache_drive[(lat2, lon2)]

            route = nx.shortest_path(G_drive, orig_node, dest_node, weight='length')
            print(type(route))
            distance = sum(ox.utils_graph.get_route_edge_attributes(G_drive, route, 'length'))
            return round(distance)

        case "walk":
            if (lat1, lon1) not in nearest_nodes_cache_walk: nearest_nodes_cache_walk[(lat1, lon1)] = ox.distance.nearest_nodes(G_walk, lon1, lat1)
            if (lat2, lon2) not in nearest_nodes_cache_walk: nearest_nodes_cache_walk[(lat2, lon2)] = ox.distance.nearest_nodes(G_walk, lon2, lat2)

            orig_node, dest_node = nearest_nodes_cache_walk[(lat1, lon1)], nearest_nodes_cache_walk[(lat2, lon2)]

            route = nx.shortest_path(G_walk, orig_node, dest_node, weight='length')
            distance = sum(ox.utils_graph.get_route_edge_attributes(G_walk, route, 'length'))
            return round(distance)




with open("address_coords.json", 'r') as read_file:
    address_dict = json.load(read_file)

drive_dict, walk_dict = pd.DataFrame(columns=pd.DataFrame(address_dict).columns).to_dict(), pd.DataFrame(columns=pd.DataFrame(address_dict).columns).to_dict()
for i in tqdm(drive_dict, desc="Progress ", ncols=200):
    drive_dict[i]: dict = {j: calculate_distance(address_dict[i][0], address_dict[i][1], address_dict[j][0], address_dict[j][1], "drive") for j in drive_dict}
    walk_dict[i]: list = {j: calculate_distance(address_dict[i][0], address_dict[i][1], address_dict[j][0], address_dict[j][1], "walk") for j in walk_dict}

write_data("cache_drive.yaml", nearest_nodes_cache_drive, 'yaml')
write_data("cache_walk.yaml", nearest_nodes_cache_walk, "yaml")
write_data("distance_drive.json", drive_dict, "json")
write_data('distance_walk.json', walk_dict, "json")


