import json

with open('address_coords_for_calculate.json', 'r') as read_file:
    d = json.load(read_file)
    print(list(d.keys())[:30])