from tools import *


def calc_min_marshr(graph, shop_box):
    count_vert = 0
    min_answer = [[], 100000]
    answer = [[], 100000]
    for i in range(1, len(graph.vertexs)):
        min_answer = [[], 100000]
        current_ver = graph.vertexs['client']

        # for vert in graph.vertexs:




def calc_min_price(graph, shop_box):
    min_price = 0
    min_path = []
    product_dict = {}
    for i in shop_box:
        shops = {}
        for ver in graph.vertexs:
            if i in graph.vertexs[ver].all_products:
                shops[ver] = graph.vertexs[ver].all_products[i]
        product_dict[i] = shops
    print('start')
    print(product_dict)
    print('sort')
    sorted_data = {}
    for product, shops in product_dict.items():
        sorted_shops = sorted(shops.items(), key=lambda x: (x[1][0], -x[1][1]))
        sorted_data[product] = [{shop[0]: shop[1]} for shop in sorted_shops]

    print(sorted_data)
    print('shop_box')
    print(shop_box)
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
        min_path.append('|')
    print('answer: ')
    print(min_path)
    print(min_price)





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
graph.add_edge('1', '2', 1000)
graph.add_edge('1', '3', 100)
graph.add_edge('2', '3', 250)
# graph.show_edges()

# shop_box = {'pizza' : 27, 'beer' : 2, 'beer2': 49}
# calc_min_price(graph, shop_box)
# shop_box = {'pizza' : 1, 'beer' : 2, 'beer2': 4}
# calc_min_price(graph, shop_box)
# shop_box = {'pizza' : 37, 'beer' : 19, 'beer2': 29}
# calc_min_price(graph, shop_box)

