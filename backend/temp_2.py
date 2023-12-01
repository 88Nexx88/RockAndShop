import time
import osmnx as ox

from calculate_distance import calculate_for_user, get_addresses_shops
G_drive, G_walk = ox.load_graphml('drive.graphml'), ox.load_graphml('walk.graphml')

# dowload_graph('Россия, Владимирская область', 'walk.graphml', 'walk')
# a = calculate_for_user(user_address="Владимир, Горького 87", shop_addresses= get_addresses_shops(), flag="walk")

while True:
    question = input("Write: ")
    match question:
        case '1':
            address = input("Write address user: ")
            start: time = time.time()
            for i in calculate_for_user(address, get_addresses_shops(), 'walk', G_drive, G_walk):
                print(i)
            print(f"run ---- {time.time() - start} sec")
        case '2':
            break
# for i in a:
#     print(i, a[i])

# qgis,





