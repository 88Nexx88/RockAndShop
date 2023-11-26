from tools import *


def calc_min_marshr(graph, shop_box):
    count_vert = 0
    min_answer = [[], 100000]
    answer = [[], 100000]
    for i in range(1, len(graph.vertexs)):
        min_answer = [[], 100000]
        current_ver = graph.vertexs['client']

        # for vert in graph.vertexs:




def calc_min_price():
    pass

graph = Graph()
graph.add_vertex('1', ['pizza', 'beer', 'vodka'], [500, 100, 350], [11, 34, 12])
graph.add_vertex('2', ['pizza', 'beer', 'beer2'], [500, 110, 120], [3, 12, 13])
graph.add_vertex('3', ['pizza', 'beer', 'beer2'], [490, 130, 110], [12, 1, 16])
graph.add_vertex('client', [], [], [])
graph.show_all_vertices()
graph.add_edge('client', '1', 250)
graph.add_edge('client', '2', 1150)
graph.add_edge('client', '3', 350)
graph.add_edge('1', '2', 1000)
graph.add_edge('1', '3', 100)
graph.add_edge('2', '3', 250)
graph.show_edges()

shop_box = {'pizza' : 22, 'beer' : 2, 'beer2': 13}