class Graph:
    def __init__(self, vertices):
        self.v = vertices  # количество вершин
        self.graph = {}  # словарь для хранения графа

    def add_edge(self, start, end, distance, max_product):
        if start not in self.graph:
            self.graph[start] = []
        self.graph[start].append((end, distance, max_product))

    def find_shortest_path(self, start, depth, shop_box, client, min_distance, stop, path, current_distance,
                           current_max_product, visited):
        if depth == 0:
            return

        for neighbor, distance, max_product in self.graph[start]:
            if neighbor not in visited and current_distance + distance <= min_distance:
                if current_max_product + max_product <= shop_box:
                    path.append(neighbor)
                    current_distance += distance
                    current_max_product += max_product

                    if current_distance < min_distance and current_max_product == shop_box:
                        min_distance = current_distance
                        stop[0] = 1  # установка стопа в случае обновления минимального расстояния

                    self.find_shortest_path(neighbor, depth - 1, shop_box, client, min_distance, stop, path,
                                            current_distance, current_max_product, visited + [neighbor])

                    path.pop()
                    current_distance -= distance
                    current_max_product -= max_product

    def run_algorithm(self, client, depth, shop_box):
        stop = [0]  # массив, чтобы иметь возможность изменить значение во внутренней функции
        path = [client]  # начальная вершина
        visited = [client]
        min_distance = float(
            'inf')  # использование бесконечности для установки начального значения минимального расстояния
        current_distance = 0
        current_max_product = 0

        self.find_shortest_path(client, depth, shop_box, client, min_distance, stop, path, current_distance,
                                current_max_product, visited)

        if stop[0] == 1:
            print("Путь всех комбинаций оказался больше минимального")
        else:
            print("Минимальное расстояние:", min_distance)


g = Graph(5)  # пример для графа с 5 вершинами

g.add_edge(0, 1, 10, 5)
g.add_edge(0, 2, 4, 2)
g.add_edge(1, 3, 12, 8)
g.add_edge(2, 3, 7, 3)
g.add_edge(3, 4, 5, 5)

g.run_algorithm(0, 3,
                7)  # Запуск алгоритма с начальной вершиной 0, глубиной поиска 3 и максимальным количеством товара 10