import json

from calculate_distance import calculate_distance_for_user
from get_geocode import geocode

from time import time
addr = input("addr: ")
start = time()

t = calculate_distance_for_user(geocode(addr), 'walking')

print("running - ", time() - start)

for k,v in t.items():
    print(k,v)
