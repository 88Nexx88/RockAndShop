
class Vertex():
    def __init__(self, name):
        self.name = name
        self.all_products = {}
        self.neighbors = {}

    def add_product(self, name, price, max_counts):
        self.all_products[name] = [price, max_counts]

    def show_edges(self):
        for i in self.neighbors:
            print(f'{self.name} -{self.neighbors[i]}-> {i}')
class Graph:
    def __init__(self):
        self.vertexs = {}

    # Добавляем новую вершину
    def add_vertex(self, name, all_product, all_price, all_max_counts):
        if name in self.vertexs:
            raise ValueError("Вершина с таким именем уже существует!")
        vert = Vertex(name)
        for index, pr in enumerate(all_product):
            vert.add_product(pr, all_price[index], all_max_counts[index])
        self.vertexs[name] = vert
        return self.vertexs[name]

    # Удаляем вершину
    def remove_vertex(self, name):
        if name not in self.vertexs:
            raise ValueError("Вершина не существует!")
        del self.vertexs[name]

    # Показываем все вершины
    def show_all_vertices(self):
        for name in self.vertexs:
            print(f'Магазин: {name}')
            for value in self.vertexs[name].all_products:
                print(f"Название: {value} Стоимость: {self.vertexs[name].all_products[value][0]} Максимальное количество: {self.vertexs[name].all_products[value][1]}")


    # Добавляем ребро
    def add_edge(self, name1, name2, value):
        if (name1 in self.vertexs) and (name2 in self.vertexs):
            self.vertexs[name1].neighbors[name2] = value
            self.vertexs[name2].neighbors[name1] = value
        else:
            raise ValueError("Вершина не существует!")

    def show_edges(self):
        for i in self.vertexs:
            self.vertexs[i].show_edges()



