import json
import os.path
import time

import osmnx as ox
import networkx as nx
import pandas as pd
import yaml
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from geopy import Yandex


# Загрузка графов Владимирской области с дорогами для пешехода и автомобиля
# G_drive, G_walk = ox.load_graphml('drive.graphml'), ox.load_graphml('walk.graphml')


# Получение координат адресов из их названия
def geocode_addresses(addresses: list) -> list:
    geolocator = Yandex(api_key="25e47a4c-c864-4761-8293-337aada63361")
    return [(geolocator.geocode(address).latitude, geolocator.geocode(address).longitude) for address in addresses if geolocator.geocode(address) is not None]


# Функция, скачивающая заданную местность в виде графа с возможностью выбора дорог для автомобиля и пешехода.
def dowload_graph(name_place: str, filename: str, flag: str):
    G = ox.graph_from_place(name_place, network_type=flag)
    ox.save_graphml(G, filename)



def write_data(filename: str, current_dict: dict, flag: str):
    with open(filename, 'w') as write_file:
        match flag:
            case "json": json.dump(current_dict, write_file, indent=3, ensure_ascii=False)

            case "yaml": yaml.dump(current_dict, write_file, default_flow_style=False)
# Реализация корректного чения кеша координат - расстояний из yaml файла в словарь
def tuple_constructor(loader, node) -> tuple: return tuple(loader.construct_sequence(node))

if os.path.exists("cache_walk.yaml") and os.path.exists("cache_drive.yaml"):
    # Зарегистрируем конструктор для тега 'tag:yaml.org,2002:python/tuple'
    yaml.SafeLoader.add_constructor('tag:yaml.org,2002:python/tuple', tuple_constructor)
    # Импорт кеша координаты - расстояние
    with open('cache_walk.yaml', 'r') as yaml_file: nearest_nodes_cache_walk = yaml.safe_load(yaml_file)

    with open('cache_drive.yaml', 'r') as yaml_file: nearest_nodes_cache_drive = yaml.safe_load(yaml_file)

else:   nearest_nodes_cache_drive, nearest_nodes_cache_walk = dict(), dict()


# Главная функция для вычисления расстояний между двумя точками
def calculate_distance(lat1, lon1, lat2, lon2, flag: str, G_drive, G_walk) -> int:
    global nearest_nodes_cache_drive, nearest_nodes_cache_walk
    start = time.time()
    match flag:
        # Для автомобилей
        case "drive":
            if (lat1, lon1) not in nearest_nodes_cache_drive: nearest_nodes_cache_drive[(lat1, lon1)] = ox.distance.nearest_nodes(G_drive, lon1, lat1)

            if (lat2, lon2) not in nearest_nodes_cache_drive: nearest_nodes_cache_drive[(lat2, lon2)] = ox.distance.nearest_nodes(G_drive, lon2, lat2)

            orig_node, dest_node = nearest_nodes_cache_drive[(lat1, lon1)], nearest_nodes_cache_drive[(lat2, lon2)]

            route = nx.shortest_path(G_drive, orig_node, dest_node, weight='length')
            # print(type(route))
            distance = sum(ox.utils_graph.get_route_edge_attributes(G_drive, route, 'length'))
            # print(f"run calculate - {time.time() - start} sec")
            return round(distance)
        # Для пешеходов
        case "walk":
            # Определение расстояния до ближайших узлов в графе, если они уже не были вычислены и не сохранены в кеше
            if (lat1, lon1) not in nearest_nodes_cache_walk: nearest_nodes_cache_walk[(lat1, lon1)] = ox.distance.nearest_nodes(G_walk, lon1, lat1)
            if (lat2, lon2) not in nearest_nodes_cache_walk: nearest_nodes_cache_walk[(lat2, lon2)] = ox.distance.nearest_nodes(G_walk, lon2, lat2)
            # Определение source и target
            orig_node, dest_node = nearest_nodes_cache_walk[(lat1, lon1)], nearest_nodes_cache_walk[(lat2, lon2)]
            # Построение кратчайшего маршрута от source до target по алгоритму Дейкстры (самый эфективный - проверено!)
            route = nx.shortest_path(G_walk, orig_node, dest_node, weight='length', method='dijkstra')
            # Получение расстояния от source до target, путем сложения весов ребер в кратчайшем пути
            distance = sum(ox.utils_graph.get_route_edge_attributes(G_walk, route, 'length'))
            # print(f"run calculate - {time.time() - start} sec")
            return round(distance)

with open("address_coords.json", 'r') as read_file:
    address_dict = json.load(read_file)

# Функция, которая вычисляет расстояния откаждого магазина до каждого
def calculate_for_shops():
    drive_dict, walk_dict = pd.DataFrame(columns=pd.DataFrame(address_dict).columns).to_dict(), pd.DataFrame(columns=pd.DataFrame(address_dict).columns).to_dict()
    for i in tqdm(drive_dict, desc="Progress ", ncols=200):
        drive_dict[i]: dict = {j: calculate_distance(address_dict[i][0], address_dict[i][1], address_dict[j][0], address_dict[j][1], "drive") for j in drive_dict}
        walk_dict[i]: list = {j: calculate_distance(address_dict[i][0], address_dict[i][1], address_dict[j][0], address_dict[j][1], "walk") for j in walk_dict}
    write_data("cache_drive.yaml", nearest_nodes_cache_drive, 'yaml')
    write_data("cache_walk.yaml", nearest_nodes_cache_walk, "yaml")
    write_data("distance_drive.json", drive_dict, "json")
    write_data('distance_walk.json', walk_dict, "json")


def get_addresses_shops() -> list:
    return [_ for _ in address_dict]

# Функция, вычисляющая расстояние от пользователя до заданной точки.
def calculate_for_user(user_address: str, shop_addresses: list, flag: str, G_drive, G_walk):
    final_dict_distaces: dict = {}
    for shop_address in shop_addresses:
        try:
            user_lat, user_lon = address_dict[user_address][0], address_dict[user_address][1]
        except:
            user_coords = geocode_addresses([user_address])[0]
            # Широта и долгота текущего местонахождения пользователя
            user_lat, user_lon = user_coords[0], user_coords[1]
        # Широта и долгота местонахождения магазина.
        try:
            shop_lat, shop_lon = address_dict[shop_address][0], address_dict[shop_address][1]
        except:
            shop_coords = geocode_addresses([shop_address])[0]
            shop_lat, shop_lon = shop_coords[0], shop_coords[1]
        final_dict_distaces[shop_address] = calculate_distance(user_lat, user_lon, shop_lat, shop_lon, flag, G_drive, G_walk)

    # запись в файл с кешем для предотвращения повторных вычислений расстояний для данных координат
    write_data("cache_drive.yaml", nearest_nodes_cache_drive, 'yaml')
    write_data("cache_walk.yaml", nearest_nodes_cache_walk, "yaml")

    # Вычисление расстояния между пользователем и магазином (в метрах)
    return final_dict_distaces

if __name__ == "__main__":
    G_drive, G_walk = ox.load_graphml('drive.graphml'), ox.load_graphml('walk.graphml')
    while True:
        question = input("Write: ")
        match question:
            case '1':
                address = input("Write address user: ")
                start: time = time.time()
                for i in calculate_for_user(address, get_addresses_shops(), 'drive', G_drive, G_walk):
                    print(i)
                print(f"run ---- {time.time() - start} sec")
            case '2':
                break
