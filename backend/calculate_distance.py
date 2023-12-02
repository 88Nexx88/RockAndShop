import json

import requests
def calculate_distance_for_user(start_coords_, flag: str) -> dict:
    # Координаты начальной и конечной точек
    # start_coords = "40.360264,56.106354"
    # end_coords = "40.365636,56.106273"
    # start_coords = str(tuple(start_coords_[::-1])).replace(" ", "").replace("(", "").replace(")", "")
    start_coords = ",".join(map(str, reversed(start_coords_)))
    dict_of_distances: dict = {}
    with open("address_coords_for_calculate.json", 'r') as read_file:
        address_coords = json.load(read_file)
    for k, end_coords in address_coords.items():
        # URL эндпоинта маршрута
        url = f"http://router.project-osrm.org/route/v1/{flag}/{start_coords};{end_coords}?overview=false"

        # Отправка GET-запроса к API
        response = requests.get(url)

        # Обработка JSON-ответа
        data = response.json()

        # Извлечение расстояния (в метрах) из ответа
        dict_of_distances[k] = data["routes"][0]["distance"]
        # print(f"Расстояние между точками: {distance_in_meters} метров")
    return dict_of_distances







