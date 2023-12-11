import time

from backend.calculate_distance import calculate_distance_for_user
from backend.get_geocode import geocode

from scipy.optimize import linprog
from backend.tools import *



class Calc_distance():

    def __init__(self, shop_box, graph):
        self.another_answer = []
        self.shop_box = shop_box
        self.graph = graph
    def create_answer(self, path):
        answer = {}
        current_shop_box = dict(self.shop_box.items())
        for i in range(1, len(path)):
            all_product = {}
            for product in self.shop_box:
                if product in self.graph.vertexs[path[i]].all_products:
                    if current_shop_box[product] == 0:
                        pass
                    elif self.graph.vertexs[path[i]].all_products[product][1] >= current_shop_box[product]:
                        all_product[product] = current_shop_box[product]
                        current_shop_box[product] = 0
                    else:
                        all_product[product] = self.graph.vertexs[path[i]].all_products[product][1]
                        current_shop_box[product] = current_shop_box[product] - \
                                                    self.graph.vertexs[path[i]].all_products[product][1]
            answer[self.graph.vertexs[path[i]].name] = all_product

        return answer


    def calculate_price_shops(self, shops):
        price = 0
        current_shop_box = dict(self.shop_box.items())
        for shop in shops:
            for product in shops[shop]:
                price += self.graph.vertexs[shop].all_products[product][0] * shops[shop][product]

        return price

    def calculate_price(self, path):
        price = 0
        current_shop_box = dict(self.shop_box.items())
        for i in range(1, len(path)):
            for product in self.shop_box:
                if product in self.graph.vertexs[path[i]].all_products:
                    if current_shop_box[product] == 0:
                        pass
                    elif self.graph.vertexs[path[i]].all_products[product][1] >= current_shop_box[product]:
                        price += current_shop_box[product] * self.graph.vertexs[path[i]].all_products[product][0]
                        current_shop_box[product] = 0
                    else:
                        price += self.graph.vertexs[path[i]].all_products[product][1] * self.graph.vertexs[path[i]].all_products[product][0]
                        current_shop_box[product] = current_shop_box[product] - \
                                                    self.graph.vertexs[path[i]].all_products[product][1]

        return price


    # def get_combinations_with_all(self, vertex, depth, current_depth=0, path=None, result=None):
    #     if path is None:
    #         path = [vertex]
    #     if current_depth == depth:
    #         if self.calculete_shop_box(path):
    #             s = self.calculate_price(path)
    #             r = self.calculate_distance(path)
    #             self.stop += 1
    #             if r < self.max_path['dist']:
    #                 if s < self.max_price['price']:
    #                 # доделать рекомендованные ещё!
    #                     self.opt_answer.append({'dist':r, 'price':s, 'path':path[:], 'shops':self.create_answer(path), 'depth':current_depth})
    #         # для тестов
    #         # result.append((path[:], self.calculate_distance(path), self.calculete_shop_box(path)))
    #         return 0
    #
    #     for neighbor, distance in self.graph.vertexs[vertex].neighbors.items():
    #         if neighbor in path:
    #             continue
    #         if self.graph.vertexs[vertex].neighbors[neighbor] + self.calculate_distance(path) > (self.min_path['dist'] + self.max_path['dist']) / 2:
    #             continue
    #         if self.calculate_price(path) > self.max_price['price']:
    #             continue
    #
    #
    #         path.append(neighbor)
    #         self.get_combinations_with_all(neighbor, depth, current_depth + 1, path, result)
    #         path.pop()
    #
    #     return result

    def get_combinations_modern(self, vertex, depth, current_depth=0, path=None, result=None):
        pass

    def get_combinations_with_distance(self, vertex, depth, current_depth=0, path=None, result=None):
        if path is None:
            path = [vertex]
        if result is None:
            result = []
        if current_depth == depth:
            r = self.calculate_distance(path)
            self.stop += 1
            if self.calculete_shop_box(path):
                if r < self.min_answer_dist['dist']:
                    # доделать рекомендованные ещё!
                    if self.min_answer_dist['depth'] != 10000 and self.min_answer_dist['depth'] < current_depth:
                        # print('!',r, '!', self.min_answer_dist['dist'], self.min_answer_dist['depth'], current_depth)
                        self.another_answer.append(self.min_answer_dist.copy())
                    self.min_answer_dist['dist'] = r
                    self.min_answer_dist['path'] = path[:]
                    self.min_answer_dist['price'] = self.calculate_price(path)
                    self.min_answer_dist['shops'] = self.create_answer(path)
                    self.min_answer_dist['depth'] = current_depth
            # для тестов
            # result.append((path[:], self.calculate_distance(path), self.calculete_shop_box(path)))
            return result

        for neighbor, distance in self.graph.vertexs[vertex].neighbors.items():
            if neighbor in path:
                continue
            if self.graph.vertexs[vertex].neighbors[neighbor] + self.calculate_distance(path) > self.min_answer_dist[
                'dist']:
                continue
            path.append(neighbor)
            self.get_combinations_with_distance(neighbor, depth, current_depth + 1, path, result)
            path.pop()

        return result

    def calculete_shop_box(self, path):
        current_shop_box = dict(self.shop_box.items())
        for i in range(1, len(path)):
            for product in self.shop_box:
                if product in self.graph.vertexs[path[i]].all_products:
                    if current_shop_box[product] == 0:
                        pass
                    elif self.graph.vertexs[path[i]].all_products[product][1] >= current_shop_box[product]:
                        current_shop_box[product] = 0
                    else:
                        current_shop_box[product] = current_shop_box[product] - \
                                                    self.graph.vertexs[path[i]].all_products[product][1]
        for product in current_shop_box:
            if current_shop_box[product] != 0:
                return False
        return True

    def calculate_distance(self, path):
        distance = 0
        for i in range(len(path) - 1):
            distance += self.graph.vertexs[path[i]].neighbors[path[i + 1]]
        return distance


    # def calc_all_path(self, graph, shop_box, min_price, min_path):
    #     self.opt_answer = []
    #
    #     self.min_path = min_path.copy()
    #     self.max_path = min_price.copy()
    #
    #     self.min_price = min_price.copy()
    #     self.max_price = min_path.copy()
    #
    #
    #
    #     self.shop_box = shop_box
    #     self.graph = graph
    #     self.stop = 0
    #     start_vertex = 'client'
    #     current_shop_box = shop_box.copy()
    #     for i in range(len(min_path['shops'].keys()), len(min_price['shops'].keys())+1):
    #         depth = i
    #         print(depth)
    #         self.get_combinations_with_all(start_vertex, depth)
    #
    #         # для тестов
    #         # print(f'{depth}____________________________')
    #         # print(self.stop)
    #         # print(f'answer ', self.min_answer_dist)
    #         # combinations_with_distance = self.get_combinations_with_distance(start_vertex, depth)
    #         # print(combinations_with_distance)
    #
    #     # print(f'Answer dist = ', self.min_answer_dist)
    #     print(f'opt answer = ', self.opt_answer)

    def calc_min_path(self, graph, shop_box, max_path):
        self.another_answer = []
        self.min_answer_dist = {'dist': 100000, 'depth': 10000}
        self.shop_box = shop_box
        self.graph = graph
        self.stop = 0
        start_vertex = 'client'
        current_shop_box = shop_box.copy()
        for i in range(1, len(max_path['shops'].keys())+1):
            depth = i
            self.get_combinations_with_distance(start_vertex, depth)

            # для тестов
            # print(f'{depth}____________________________')
            # print(self.stop)
            # print(f'answer ', self.min_answer_dist)
            # combinations_with_distance = self.get_combinations_with_distance(start_vertex, depth)
            # print(combinations_with_distance)

        # print(f'Answer dist = ', self.min_answer_dist)
        # print(f'another answer = ', self.another_answer)
        # print(f'answer = ', self.min_answer_dist)
        return self.min_answer_dist


def calc_(result):
    min_price_answer = create_answer_min_price(result)
    all_answer = create_answer_all(result, min_price_answer)
    # for a in all_answer:
    #     print(a, all_answer[a])

    for a in all_answer:
        if type(all_answer[a]) == type(dict()):
            print(f"{a} - {all_answer[a]['dist']} - {all_answer[a]['price']}")
        else:
            for i, _  in enumerate(all_answer[a]):
                print(f"{a} - {all_answer[a][i]['dist']} - {all_answer[a][i]['price']}")

    return all_answer


def create_answer_min_path(data, current_path):
    kost = 'Владимир '
    start = time.time()
    shop_box = {}
    for i, val in enumerate(data['products']):
        shop_box[val] = int(data['user_counts'][i])

    all_path = {}
    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            if kost not in val:
                val = kost+val
            all_path[val] = [10000000 for i in range(len(shop_box.keys()))]

    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            if kost not in val:
                val = kost+val
            all_path[val][index] = current_path['client'][val] / data['user_counts'][index]


    all_price = {}
    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            if kost not in val:
                val = kost+val
            all_price[val] = [10000 for i in range(len(shop_box.keys()))]

    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            if kost not in val:
                val = kost+val
            all_price[val][index] = data['prices'][index][ind]

    all_counts = {}
    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            if kost not in val:
                val = kost+val
            all_counts[val] = [0 for i in range(len(shop_box.keys()))]

    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            if kost not in val:
                val = kost+val
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
        for key in all_path:
            a.append(all_path[key][count])
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
    # print('Цена Расстоянием: ', answer['fun'])
    min_price_answer = {'price': answer['fun']}
    shops = {}
    for index, shop in enumerate(list(all_counts.keys())):
        # print(shop)
        count = 0
        ans = f'{shop}\n'
        flag = 0
        products = {}
        for product in shop_box.keys():
            ans += product + ' '+str(answer['x'][index + count]) + '\n'
            if answer['x'][index + count] != 0:
                products[product] = answer['x'][index + count]
                flag += 1
            count += len(list(all_counts.keys()))
        if flag != 0:
            pass
            # print(ans)
        if len(products) != 0:
            shops[shop] = products

    finish = time.time()
    min_price_answer['shops'] = shops
    # print(min_price_answer)
    print('Время мин пути', finish-start)
    return min_price_answer

def create_answer_all(data, min_price_answer):
    shop_box = {}
    for i, val in enumerate(data['products']):
        shop_box[val] = int(data['user_counts'][i])

    shops = {}
    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            shops[val] = {}
            shops[val]['prices'] = []
            shops[val]['count'] = []
            shops[val]['product'] = []
    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            shops[val]['prices'].append(data['prices'][index][ind])
            shops[val]['count'].append(data['counts'][index][ind])
            shops[val]['product'].append(data['products'][index])

    # print(shops)
    s = shops.keys()
    edges = calc_edge(s, data['adress'], 0 if data['mode1'] == 'Пешком' else 1)
    #
    graph = Graph()
    graph.add_vertex('client', [], [], [])
    for shop, value in shops.items():
        if 'Владимир' not in shop:
            graph.add_vertex('Владимир ' + shop, value['product'], value['prices'], value['count'])
        else:
            graph.add_vertex(shop, value['product'], value['prices'], value['count'])
    # print(len(edges))
    # print('________________________')
    for first in edges:
        # print(len(edges[first]))
        for second in edges[first]:
            graph.add_edge(first, second, edges[first][second])
    # print('________________________')
    # graph.print_all_param()

    max_path_answer = create_answer_min_path(data, edges)

    cl = Calc_distance(shop_box, graph)
    list_name = ['client']
    for shop1 in list(min_price_answer['shops'].keys()):
        if 'Владимир ' not in shop1:
            list_name.append('Владимир '+shop1)
        else:
            list_name.append(shop1)

    max_path_answer['path'] = list(max_path_answer['shops'].keys())
    max_path_answer['path'].append('client')
    max_path_answer['tsp'], max_path_answer['dist'] = graph.calc_distance(max_path_answer['path'])

    start = time.time()
    if len(shop_box) < 12:
        start = time.time()
        min_dist_answer = cl.calc_min_path(graph, shop_box, max_path_answer)
        min_dist_answer['tsp'], min_dist_answer['dist'] = graph.calc_distance(min_dist_answer['path'])
        finish = time.time()
        print(f'Время мин расстояния {finish - start}')
    else:
        min_dist_answer = {}


    max_path_answer['price'] = cl.calculate_price_shops(max_path_answer['shops'])


    min_price_answer['path'] = list_name
    min_price_answer['tsp'], min_price_answer['dist'] = graph.calc_distance(min_price_answer['path'])
    # min_price_answer['price'] = cl.calculate_price_shops(min_price_answer['shops'])



    # start = time.time()
    opt_answer = create_answer_min_path_price(data, edges)
    for index, ans in enumerate(opt_answer):
        f = list(opt_answer[index]['shops'].keys())
        f.append('client')
        opt_answer[index]['path'] = f
        opt_answer[index]['tsp'], opt_answer[index]['dist'] = graph.calc_distance(f)
        opt_answer[index]['price'] = cl.calculate_price_shops(opt_answer[index]['shops'])
    if len(shop_box) < 12:
        opt_answer.append(max_path_answer)
    else:
        min_dist_answer = max_path_answer.copy()
    for i in cl.another_answer:
        # print(i['path'])
        i['tsp'], i['dist'] = graph.calc_distance(i['path'])
        i['price'] = cl.calculate_price_shops(i['shops'])
        opt_answer.append(i)
    optimal_answer = []
    optimal_answer2 = []
    # print(opt_answer)
    for index, ans in enumerate(opt_answer):
        if (opt_answer[index]['dist'] < min_price_answer['dist'] and opt_answer[index]['price'] < min_dist_answer['price']):
            if ((opt_answer[index]['price'] > min_price_answer['price'] and opt_answer[index]['dist'] > min_dist_answer['dist'])):
                optimal_answer.append(opt_answer[index])
    unique_options = []
    seen = set()


    # print(len(opt_answer), len(optimal_answer), len(optimal_answer2))

    # print(opt_answer)
    # opt_answer = cl.calc_all_path(graph, shop_box, min_price_answer, min_dist_answer)
    # finish = time.time()
    # print(f'Vremy ^ {finish - start}')


    for option in optimal_answer:
        option_tuple = (option['price'], option['dist'])
        if option_tuple not in seen:
            unique_options.append(option)
            seen.add(option_tuple)

    optimal_answer = unique_options.copy()

    # проверка минимальных ответов
    if min_price_answer['price'] == min_dist_answer['price']:
        optimal_answer = [min_dist_answer]
    if min_price_answer['dist'] == min_dist_answer['dist']:
        optimal_answer = [min_price_answer]
    if len(optimal_answer) == 0:
        optimal_answer.append(min_dist_answer)
        optimal_answer.append(min_price_answer)
    best_answer = {}
    min_dist = 10000000
    min_price = 10000000
    for answ in optimal_answer:
        if min_dist >= abs(answ['dist'] - min_dist_answer['dist']):
            if min_price >= abs(answ['price'] - min_price_answer['price']):
                min_price = abs(answ['price'] - min_price_answer['price'])
                min_dist = abs(answ['dist'] - min_dist_answer['dist'])
                best_answer = answ
    # print('!!!', best_answer['dist'], best_answer['price'])
    for i in optimal_answer:
        print(i)
        print(i['tsp'])

    answer_all = {'price': min_price_answer, 'dist':min_dist_answer, 'opt_answer':best_answer, 'all_opt':optimal_answer}
    return answer_all
    # graph.show_all_vertices()



import json

def calc_edge(shops, address, mode):
    new_shops = []
    for shop in shops:
        if 'Владимир' not in shop:
            new_shops.append('Владимир ' + shop)
        else:
            new_shops.append(shop)
    shops = new_shops.copy()
    if mode == 0:
        with open('backend/distance_walk.json', encoding='utf-8', mode='r') as f:
            data = json.load(f)
    else:
        with open('backend/distance_drive.json', encoding='utf-8', mode='r') as f:
            data = json.load(f)
    current_data = {}
    for shop in shops:
        shop_s = {}
        for sh in data[shop]:
            if sh != shop and sh in shops:
                shop_s[sh] = data[shop][sh]
        current_data[shop] = shop_s

    start = time.time()
    client = calculate_distance_for_user(geocode(address[1]), shops,'walking' if mode == 0 else 'driving')
    shop_s = {}
    for sh in client:
        if  sh in shops:
            shop_s[sh] = client[sh]


    for sh in shop_s:
        current_data[sh]['client'] = shop_s[sh]

    current_data['client'] = shop_s
    finish = time.time()

    # for shop in current_data:
    #     print(shop, current_data[shop])

    print(f'Время рассчёта маршрутов ', finish-start)

    return current_data

def create_answer_min_path_price(data, current_path):
    kost = 'Владимир '
    start = time.time()
    count = 10
    weight_cost = 2  # Вес для стоимости
    weight_distance = -0.15  # Вес для расстояния
    # if len(shop_box) > 12:
    #     count = 4
    #     weight_cost = 1.2  # Вес для стоимости
    #     weight_distance = 0.1  # Вес для расстояния
    all_answer = []
    for i in range(count):
        shop_box = {}
        for i, val in enumerate(data['products']):
            shop_box[val] = int(data['user_counts'][i])

        weight_cost -= 0.15
        weight_distance += 0.15
        all_path = {}
        for index, d in enumerate(data['shops']):
            for ind, val in enumerate(d):
                if kost not in val:
                    val = kost + val
                all_path[val] = [10000000 for i in range(len(shop_box.keys()))]

        for index, d in enumerate(data['shops']):
            for ind, val in enumerate(d):
                if kost not in val:
                    val = kost + val
                all_path[val][index] = current_path['client'][val] / data['user_counts'][index]

        all_price = {}
        for index, d in enumerate(data['shops']):
            for ind, val in enumerate(d):
                if kost not in val:
                    val = kost + val
                all_price[val] = [10000 for i in range(len(shop_box.keys()))]

        for index, d in enumerate(data['shops']):
            for ind, val in enumerate(d):
                if kost not in val:
                    val = kost + val
                all_price[val][index] = data['prices'][index][ind]

        all_counts = {}
        for index, d in enumerate(data['shops']):
            for ind, val in enumerate(d):
                if kost not in val:
                    val = kost + val
                all_counts[val] = [0 for i in range(len(shop_box.keys()))]

        for index, d in enumerate(data['shops']):
            for ind, val in enumerate(d):
                if kost not in val:
                    val = kost + val
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
            for key in all_path:
                a.append(all_path[key][count] * weight_distance + all_price[key][count] * weight_cost)
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
        # print('Цена: ', answer['fun'])
        min_answer = {'price': answer['fun']}
        shops = {}
        for index, shop in enumerate(list(all_counts.keys())):
            # print(shop)
            count = 0
            ans = f'{shop}\n'
            flag = 0
            products = {}
            for product in shop_box.keys():
                ans += product + ' ' + str(answer['x'][index + count]) + '\n'
                if answer['x'][index + count] != 0:
                    products[product] = answer['x'][index + count]
                    flag += 1
                count += len(list(all_counts.keys()))
            if flag != 0:
                pass
                # print(ans)
            if len(products) != 0:
                shops[shop] = products


        min_answer['shops'] = shops
        all_answer.append(min_answer)
        # print(min_answer)
    finish = time.time()
    print('Время мин по цене и раст', finish - start)

    return all_answer



def create_answer_min_price(data):
    kost = 'Владимир '
    start = time.time()
    shop_box = {}
    for i, val in enumerate(data['products']):
        shop_box[val] = int(data['user_counts'][i])

    all_price = {}
    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            if kost not in val:
                val = kost + val
            all_price[val] = [10000 for i in range(len(shop_box.keys()))]

    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            if kost not in val:
                val = kost + val
            all_price[val][index] = data['prices'][index][ind]

    all_counts = {}
    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            if kost not in val:
                val = kost + val
            all_counts[val] = [0 for i in range(len(shop_box.keys()))]

    for index, d in enumerate(data['shops']):
        for ind, val in enumerate(d):
            if kost not in val:
                val = kost + val
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
    # print('Цена: ', answer['fun'])
    min_price_answer = {'price': answer['fun']}
    shops = {}
    for index, shop in enumerate(list(all_counts.keys())):
        # print(shop)
        count = 0
        ans = f'{shop}\n'
        flag = 0
        products = {}
        for product in shop_box.keys():
            ans += product + ' '+str(answer['x'][index + count]) + '\n'
            if answer['x'][index + count] != 0:
                products[product] = answer['x'][index + count]
                flag += 1
            count += len(list(all_counts.keys()))
        if flag != 0:
            pass
            # print(ans)
        if len(products) != 0:
            shops[shop] = products

    finish = time.time()
    min_price_answer['shops'] = shops
    # print(min_price_answer)
    print('Время мин цены', finish-start)
    return min_price_answer


