# import osmnx as ox
# import networkx as nx
# from folium import folium
#
# # Задаем начальную и конечную точки (координаты)
# origin = (55.7558, 37.6176)  # Москва
# destination = (55.8500, 37.6500)  # Пример конечной точки
#
# # Получаем граф OSM для автомобильных дорог
# G_drive = ox.graph_from_point(center_point=origin, dist=5000, network_type='drive')
#
# # Получаем граф OSM для дорог, по которым могут двигаться пешеходы
# G_walk = ox.graph_from_point(center_point=origin, dist=5000, network_type='walk')
#
# # Находим ближайшие узлы к начальной и конечной точкам в каждом из графов
# orig_node_drive = ox.distance.nearest_nodes(G_drive, origin[1], origin[0])
# dest_node_drive = ox.distance.nearest_nodes(G_drive, destination[1], destination[0])
#
# orig_node_walk = ox.distance.nearest_nodes(G_walk, origin[1], origin[0])
# dest_node_walk = ox.distance.nearest_nodes(G_walk, destination[1], destination[0])
#
# # Вычисляем кратчайший путь для автомобиля и пешехода
# car_route = nx.shortest_path(G_drive, orig_node_drive, dest_node_drive, weight='length')
# pedestrian_route = nx.shortest_path(G_walk, orig_node_walk, dest_node_walk, weight='length')
#
# # Вычисляем расстояние для автомобильного и пешеходного маршрутов
# car_distance = sum(ox.utils_graph.get_route_edge_attributes(G_drive, car_route, 'length'))
# pedestrian_distance = sum(ox.utils_graph.get_route_edge_attributes(G_walk, pedestrian_route, 'length'))
#
# print(f"car distance - {car_distance} m")
# print(f"walk distance - {pedestrian_distance} m")
#
# # Предполагаемые скорости передвижения (в м/с)
# car_speed = 13.89  # примерно 50 км/ч
# pedestrian_speed = 1.39  # примерно 5 км/ч
#
# # Рассчитываем время в пути (в секундах)
# car_time_seconds = car_distance / car_speed
# pedestrian_time_seconds = pedestrian_distance / pedestrian_speed
#
# # Преобразуем время в пути из секунд в минуты
# car_time_minutes = car_time_seconds / 60
# pedestrian_time_minutes = pedestrian_time_seconds / 60
#
# print(f"Примерное время в пути для автомобиля: {car_time_minutes:.2f} минут")
# print(f"Примерное время в пути для пешехода: {pedestrian_time_minutes:.2f} минут")
#

#------------------------------------------------------------------------------------------------------------------------


import osmnx as ox
import networkx as nx
import folium

# # Задаем начальную и конечную точки (координаты)
# origin = (55.7558, 37.6176)  # Москва
# destination = (55.8500, 37.6500)  # Пример конечной точки
#
# # Получаем граф OSM для автомобильных дорог
# G_drive = ox.graph_from_point(center_point=origin, dist=5000, network_type='drive')
#
# # Получаем граф OSM для дорог, по которым могут двигаться пешеходы
# G_walk = ox.graph_from_point(center_point=origin, dist=5000, network_type='walk')
#
# # Находим ближайшие узлы к начальной и конечной точкам в каждом из графов
# orig_node_drive = ox.distance.nearest_nodes(G_drive, origin[1], origin[0])
# dest_node_drive = ox.distance.nearest_nodes(G_drive, destination[1], destination[0])
#
# orig_node_walk = ox.distance.nearest_nodes(G_walk, origin[1], origin[0])
# dest_node_walk = ox.distance.nearest_nodes(G_walk, destination[1], destination[0])
#
# # Вычисляем кратчайший путь для автомобиля и пешехода
# car_route = nx.shortest_path(G_drive, orig_node_drive, dest_node_drive, weight='length')
# pedestrian_route = nx.shortest_path(G_walk, orig_node_walk, dest_node_walk, weight='length')
#
# # Отображаем маршруты на карте folium
# car_map = ox.plot_graph_folium(G_drive, route=car_route, popup_attribute='length', folium_map=None, tiles='OpenStreetMap')
# pedestrian_map = ox.plot_graph_folium(G_walk, route=pedestrian_route, popup_attribute='length', folium_map=None, tiles='OpenStreetMap')
#
# # Добавляем маркеры начальной и конечной точек
# folium.Marker(location=origin, popup='Начальная точка', icon=folium.Icon(color='green')).add_to(car_map)
# folium.Marker(location=destination, popup='Конечная точка', icon=folium.Icon(color='red')).add_to(car_map)
#
# folium.Marker(location=origin, popup='Начальная точка', icon=folium.Icon(color='green')).add_to(pedestrian_map)
# folium.Marker(location=destination, popup='Конечная точка', icon=folium.Icon(color='red')).add_to(pedestrian_map)
#
# # Сохраняем карты в HTML файлы
# car_map.save('car_route_map.html')
# pedestrian_map.save('pedestrian_route_map.html')
#----------------------------------------------------------------------------------------------------------------------------------------------


import osmnx as ox
import networkx as nx
import pandas as pd
import sqlite3

def calculate_distances_dataframe(df, db_file):
    # Создаем графы OSM для автомобильных дорог и пешеходных маршрутов
    G_drive = ox.graph_from_point(center_point=(df.iloc[0, 1], df.iloc[0, 2]), dist=5000, network_type='drive')
    G_walk = ox.graph_from_point(center_point=(df.iloc[0, 1], df.iloc[0, 2]), dist=5000, network_type='walk')

    # Создаем подключение к базе данных SQLite
    conn = sqlite3.connect(db_file)

    # Создаем пустые таблицы для расстояний
    car_distances = pd.DataFrame(index=df.index, columns=df.index)
    pedestrian_distances = pd.DataFrame(index=df.index, columns=df.index)

    for i in range(len(df)):
        for j in range(len(df)):
            # Находим ближайшие узлы в каждом графе
            orig_node_drive = ox.distance.nearest_nodes(G_drive, df.iloc[i, 2], df.iloc[i, 1])
            dest_node_drive = ox.distance.nearest_nodes(G_drive, df.iloc[j, 2], df.iloc[j, 1])
            orig_node_walk = ox.distance.nearest_nodes(G_walk, df.iloc[i, 2], df.iloc[i, 1])
            dest_node_walk = ox.distance.nearest_nodes(G_walk, df.iloc[j, 2], df.iloc[j, 1])

            # Вычисляем кратчайший путь и расстояние для автомобиля и пешехода
            car_route = nx.shortest_path(G_drive, orig_node_drive, dest_node_drive, weight='length')
            pedestrian_route = nx.shortest_path(G_walk, orig_node_walk, dest_node_walk, weight='length')
            car_distance = sum(ox.utils_graph.get_route_edge_attributes(G_drive, car_route, 'length'))
            pedestrian_distance = sum(ox.utils_graph.get_route_edge_attributes(G_walk, pedestrian_route, 'length'))

            # Записываем расстояния в таблицы
            car_distances.at[i, j] = car_distance
            pedestrian_distances.at[i, j] = pedestrian_distance

    # Сохраняем таблицы в базу данных SQLite
    car_distances.to_sql('car_distances', conn, index_label='id', if_exists='replace')
    pedestrian_distances.to_sql('pedestrian_distances', conn, index_label='id', if_exists='replace')

    # Закрываем соединение с базой данных
    conn.close()

# Пример использования:
df = pd.read_csv('coords.csv')

db_file = 'db.db3'
calculate_distances_dataframe(df, db_file)
