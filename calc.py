from tools import *


from tools import *
from  collections import deque


class Calc():
    def __init__(self):
        self.min_answer_dist = {'dist' : 1000000, 'depth' : -1, 'path' : []}
        self.min_answer_price = {'price': 1000000, 'path': []}
        self.recom_answer_price = []
        self.recom_answer_dist = []
        self.stop = 0


    def create_answer(self):
        pass
    def get_combinations_with_distance(self, graph, vertex, depth, current_depth=0, path=None, result=None):
        if path is None:
            path = [vertex]
        if result is None:
            result = []
        if current_depth == depth:
            r = self.calculate_distance(graph, path)
            self.stop+=1
            if self.calculete_shop_box(graph, path, shop_box):
                if r < self.min_answer_dist['dist']:
                    #доделать рекомендованные ещё!
                    self.min_answer_dist['dist'] = r
                    self.min_answer_dist['path'] = path[:]
                    self.min_answer_dist['depth'] = current_depth
            # для тестов
            # result.append((path[:], self.calculate_distance(graph, path), self.calculete_shop_box(graph, path, shop_box)))
            return

        for neighbor, distance in graph.vertexs[vertex].neighbors.items():
            if neighbor in path:
                continue
            if graph.vertexs[vertex].neighbors[neighbor]+self.calculate_distance(graph, path) > self.min_answer_dist['dist']:
                continue

            path.append(neighbor)
            self.get_combinations_with_distance(graph, neighbor, depth, current_depth + 1, path, result)
            path.pop()

        return result

    def calculete_shop_box(self, graph, path, shop_box):
        current_shop_box = dict(shop_box.items())
        for i in range(1, len(path)):
            for product in shop_box:
                if product in graph.vertexs[path[i]].all_products:
                    if current_shop_box[product] == 0:
                        pass
                    elif graph.vertexs[path[i]].all_products[product][1] >= current_shop_box[product]:
                        current_shop_box[product] = 0
                    else:
                        current_shop_box[product] = current_shop_box[product] - graph.vertexs[path[i]].all_products[product][1]
        for product in current_shop_box:
            if current_shop_box[product] != 0:
                return False
        return True
    def calculate_distance(self, graph, path):
        distance = 0
        for i in range(len(path) - 1):
            distance += graph.vertexs[path[i]].neighbors[path[i+1]]
        return distance


    def calc_min_path(self, graph, shop_box):
        self.shop_box = shop_box
        start_vertex = 'client'
        current_shop_box = shop_box.copy()
        for i in range(1, len(graph.vertexs)):
            depth = i
            self.get_combinations_with_distance(graph, start_vertex, depth)

            # для тестов
            # print(f'{depth}____________________________')
            # print(self.stop)
            # print(f'answer ', self.min_answer_dist)
            # combinations_with_distance = get_combinations_with_distance(graph, start_vertex, depth)
            # print(combinations_with_distance)

        print(f'Answer dist = ', self.min_answer_dist)


    def calc_min_price(self, graph, shop_box):
        min_price = 0
        min_path = ['client']
        product_dict = {}
        for i in shop_box:
            shops = {}
            for ver in graph.vertexs:
                if i in graph.vertexs[ver].all_products:
                    shops[ver] = graph.vertexs[ver].all_products[i]
            product_dict[i] = shops
        # print('start')
        # print(product_dict)
        # print('sort')
        sorted_data = {}
        for product, shops in product_dict.items():
            sorted_shops = sorted(shops.items(), key=lambda x: (x[1][0], -x[1][1]))
            sorted_data[product] = [{shop[0]: shop[1]} for shop in sorted_shops]

        # print(sorted_data)
        # print('shop_box')
        # print(shop_box)
        for i in shop_box:
            index = 0
            current_count = shop_box[i]
            while current_count != 0:
                cur = list(sorted_data[i][index].values())[0]
                if current_count - cur[1] <= 0:
                    min_path.append(list(sorted_data[i][index].keys())[0])
                    min_price += cur[0]*current_count
                    current_count -= current_count
                else:
                    min_path.append(list(sorted_data[i][index].keys())[0])
                    min_price += cur[0]*cur[1]
                    current_count -= cur[1]
                    index+=1
            # min_path.append('|')
        amswer_path = []
        for i in min_path:
            if i not in amswer_path:
                amswer_path.append(i)
        self.min_answer_price['price'] = min_price
        self.min_answer_price['path'] = amswer_path
        print(f'Answer price = {self.min_answer_price}')


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




graph = Graph()
graph.add_vertex('1', ['pizza', 'beer', 'vodka'], [500, 100, 350], [11, 34, 12])
graph.add_vertex('2', ['pizza', 'beer', 'beer2'], [500, 110, 120], [3, 12, 13])
graph.add_vertex('3', ['pizza', 'beer', 'beer2'], [490, 130, 110], [12, 1, 16])
graph.add_vertex('4', ['pizza', 'beer', 'beer2'], [490, 130, 110], [19, 19, 19])
graph.add_vertex('5', ['pizza', 'beer', 'beer2'], [490, 130, 110], [26, 20, 30])
graph.add_vertex('6', ['pizza', 'beer', 'beer2'], [490, 130, 110], [20, 26, 11])
graph.add_vertex('client', [], [], [])
# graph.show_all_vertices()
graph.add_edge('client', '1', 250)
graph.add_edge('client', '2', 1150)
graph.add_edge('client', '3', 350)
graph.add_edge('client', '4', 1250)
graph.add_edge('client', '5', 1155)
graph.add_edge('client', '6', 550)
graph.add_edge('1', '2', 1000)
graph.add_edge('1', '3', 500)
graph.add_edge('1', '4', 1000)
graph.add_edge('1', '5', 100)
graph.add_edge('1', '6', 200)
graph.add_edge('2', '3', 250)
graph.add_edge('2', '4', 350)
# graph.show_edges()


calc = Calc()
shop_box = {'pizza' : 34, 'beer' : 53, 'beer2': 12}
print(shop_box)
calc.calc_min_price(graph, shop_box)
calc.calc_min_path(graph, shop_box)

shop_box = {'pizza' : 1, 'beer' : 2, 'beer2': 4}
print(shop_box)
calc.calc_min_price(graph, shop_box)
calc.calc_min_path(graph, shop_box)


