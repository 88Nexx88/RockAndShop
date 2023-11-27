# import osmnx as ox
#
# G = ox.graph_from_place('Россия, Владимирская область', network_type='walk')
# ox.save_graphml(G,'walk.graphml')

import yaml

my_dict = {("key1", "subkey"): 13.23, ("key2", "subkey"): "value2"}

with open('data.yaml', 'w') as yaml_file:
    yaml.dump(my_dict, yaml_file, default_flow_style=False)

import yaml

def tuple_constructor(loader, node):
    return tuple(loader.construct_sequence(node))

# Зарегистрируем конструктор для тега 'tag:yaml.org,2002:python/tuple'
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:python/tuple', tuple_constructor)

with open('data.yaml', 'r') as yaml_file:
    data_tuples = yaml.safe_load(yaml_file)

print(type(data_tuples[('key1', 'subkey')]))


print(round(12.232430746))