import json

import requests
from calculate_distance_old import get_addresses_shops
def geocode(address):
    # URL для запроса к Nominatim
    nominatim_url = "https://nominatim.openstreetmap.org/search"

    # Параметры запроса
    params = {
        'q': address,
        'format': 'json',  # формат ответа
    }

    # Отправляем GET-запрос к Nominatim
    response = requests.get(nominatim_url, params=params)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Парсим JSON-ответ
        data = response.json()

        # Проверяем, есть ли результаты
        if data:
            # Получаем координаты первого результата
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return [lat, lon]
        else:
            print("Адрес не найден.", address)
    else:
        print(f"Ошибка запроса: {response.status_code}")

# Пример использования
# address = "Владимир, Балакирева 28"
# coordinates = geocode(address)
# if coordinates:
#     print(f"Координаты для адреса {address}: {coordinates}")


