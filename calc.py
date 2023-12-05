import random
import time

from tools import *

import numpy as np
import storage.result_find as result_
from scipy.optimize import linprog
from tools import *
from collections import deque

'''
    # def create_answer(self):
    #     pass
    # def get_combinations_with_distance(self, graph, vertex, depth, current_depth=0, path=None, result=None):
    #     if path is None:
    #         path = [vertex]
    #     if result is None:
    #         result = []
    #     if current_depth == depth:
    #         r = self.calculate_distance(graph, path)
    #         self.stop+=1
    #         if self.calculete_shop_box(graph, path, self.shop_box):
    #             if r < self.min_answer_dist['dist']:
    #                 #доделать рекомендованные ещё!
    #                 self.min_answer_dist['dist'] = r
    #                 self.min_answer_dist['path'] = path[:]
    #                 self.min_answer_dist['depth'] = current_depth
    #         # для тестов
    #         # result.append((path[:], self.calculate_distance(graph, path), self.calculete_shop_box(graph, path, shop_box)))
    #         return
    # 
    #     for neighbor, distance in graph.vertexs[vertex].neighbors.items():
    #         if neighbor in path:
    #             continue
    #         if graph.vertexs[vertex].neighbors[neighbor]+self.calculate_distance(graph, path) > self.min_answer_dist['dist']:
    #             continue
    # 
    #         path.append(neighbor)
    #         self.get_combinations_with_distance(graph, neighbor, depth, current_depth + 1, path, result)
    #         path.pop()
    # 
    #     return result
    # 
    # def calculete_shop_box(self, graph, path, shop_box):
    #     current_shop_box = dict(shop_box.items())
    #     for i in range(1, len(path)):
    #         for product in shop_box:
    #             if product in graph.vertexs[path[i]].all_products:
    #                 if current_shop_box[product] == 0:
    #                     pass
    #                 elif graph.vertexs[path[i]].all_products[product][1] >= current_shop_box[product]:
    #                     current_shop_box[product] = 0
    #                 else:
    #                     current_shop_box[product] = current_shop_box[product] - graph.vertexs[path[i]].all_products[product][1]
    #     for product in current_shop_box:
    #         if current_shop_box[product] != 0:
    #             return False
    #     return True
    # def calculate_distance(self, graph, path):
    #     distance = 0
    #     for i in range(len(path) - 1):
    #         distance += graph.vertexs[path[i]].neighbors[path[i+1]]
    #     return distance
    # 
    # 
    # def calc_min_path(self, graph, shop_box):
    #     self.shop_box = shop_box
    #     start_vertex = 'client'
    #     current_shop_box = shop_box.copy()
    #     for i in range(1, len(graph.vertexs)):
    #         depth = i
    #         self.get_combinations_with_distance(graph, start_vertex, depth)
    # 
    #         # для тестов
    #         # print(f'{depth}____________________________')
    #         # print(self.stop)
    #         # print(f'answer ', self.min_answer_dist)
    #         # combinations_with_distance = get_combinations_with_distance(graph, start_vertex, depth)
    #         # print(combinations_with_distance)
    # 
    #     print(f'Answer dist = ', self.min_answer_dist)
'''


def create_answer_min_price(data):
    start = time.time()
    shop_box = {}
    for i, val in enumerate(data['products']):
        shop_box[val] = int(data['user_counts'][i])

    all_price = {}
    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            all_price[val] = [10000 for i in range(len(shop_box.keys()))]

    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            all_price[val][index] = data['prices'][index][ind]

    all_counts = {}
    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            all_counts[val] = [0 for i in range(len(shop_box.keys()))]

    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            all_counts[val][index] = data['counts'][index][ind]

    b_ub = []
    count = 0
    for product in shop_box:
        for key in all_counts:
            b_ub.append(all_counts[key][count])
        count += 1

    a_val = []
    count = 0
    for product in shop_box:
        a = []
        for key in all_price:
            a.append(all_price[key][count])
        count += 1
        a_val.append(a)

    A = np.array(a_val)
    b_eq = list(shop_box.values())
    m, n = A.shape
    c = list(np.reshape(A, n * m))  # Преобразование матрицы A в список c.
    A_ub = np.zeros([n * m, m * n])
    for i in np.arange(0, n * m, 1):  # Заполнение матрицы условий –неравенств.
        for j in np.arange(0, n * m, 1):
            if i == j:
                A_ub[i, j] = 1

    A_eq = np.zeros([m, m * n])
    for i in np.arange(0, m, 1):  # Заполнение матрицы условий –равенств.
        for j in np.arange(i * n, n * (i + 1), 1):
            A_eq[i, j] = 1

    answer = linprog(c, A_ub, b_ub, A_eq, b_eq)
    print('Цена: ', answer['fun'])

    for index, shop in enumerate(list(all_counts.keys())):
        # print(shop)
        count = 0
        ans = f'{shop}\n'
        flag = 0
        for product in shop_box.keys():
            ans += str(answer['x'][index + count]) + '\n'
            if answer['x'][index + count] != 0:
                flag += 1
            count += len(list(all_counts.keys()))
        if flag != 0:
            print(ans)

    finish = time.time()
    print('Время ', finish-start)


def bfs_mod(self, graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    while queue:
        vertex = queue.popleft()
        print(vertex)  # Здесь можно выполнить любые операции с вершиной
        min = 10000000
        for neighbor in graph.vertexs[vertex].neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited

# # calc.create_answer_min_price(shop_box, )
# # calc.create_answer_min_price(shop_box, result)
#
# graph = Graph()
# graph.add_vertex('1', ['pizza', 'beer', 'vodka'], [500, 100, 350], [11, 34, 12])
# graph.add_vertex('2', ['pizza', 'beer', 'beer2'], [500, 110, 120], [3, 12, 13])
# graph.add_vertex('3', ['pizza', 'beer', 'beer2'], [490, 130, 110], [12, 1, 16])
# graph.add_vertex('4', ['pizza', 'beer', 'beer2'], [490, 130, 110], [19, 19, 19])
# graph.add_vertex('5', ['pizza', 'beer', 'beer2'], [490, 130, 110], [26, 20, 30])
# graph.add_vertex('6', ['pizza', 'beer', 'beer2'], [490, 130, 110], [20, 26, 11])
# graph.add_vertex('client', [], [], [])
# # graph.show_all_vertices()
# graph.add_edge('client', '1', 250)
# graph.add_edge('client', '2', 1150)
# graph.add_edge('client', '3', 350)
# graph.add_edge('client', '4', 1250)
# graph.add_edge('client', '5', 1155)
# graph.add_edge('client', '6', 550)
# graph.add_edge('1', '2', 1000)
# graph.add_edge('1', '3', 500)
# graph.add_edge('1', '4', 1000)
# graph.add_edge('1', '5', 100)
# graph.add_edge('1', '6', 200)
# graph.add_edge('2', '3', 250)
# graph.add_edge('2', '4', 350)
# # graph.show_edges()
#
#
# shop_box = {'pizza' : 34, 'beer' : 53, 'beer2': 12}
# calc = Calc(shop_box)
# shop_box = {'pizza' : 34, 'beer' : 53, 'beer2': 12}
# print(shop_box)
# calc.calc_min_path(graph, shop_box)
# #
# # shop_box = {'pizza' : 1, 'beer' : 2, 'beer2': 4}
# # print(shop_box)
# # calc.calc_min_path(graph, shop_box)
