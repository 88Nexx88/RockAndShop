class Value_page():

    def __init__(self):
        self.korzina_len = 0
        self.list_korzina = []


    def add_korzina_product(self, product):
        self.korzina_len += 1
        self.list_korzina.append(product)

    def delete_korzina_product(self, product):
        self.korzina_len -= 1
        self.list_korzina.remove(product)


class Product():

    def __init__(self, name, info, count, image, shops, price):
        self.name = name
        self.info = info
        self.count = count
        self.image = image
        self.shops = shops
        self.price = price
    


# import itertools

# s = 'матвей'
# all = []

# perm_set = itertools.permutations(s) 

# for var in perm_set: 
#     if var[0] != 'й' and var[1] != 'м':
#         print(var)
#         all.append(var)


# print((7+18, 25+18-32, 29+18 -32, 26+18-32, 15+18-32))
# print(len(all))






# def f(x, y):
#     if x > y:
#         return 0
#     if x == y:
#         return 1
#     else:
#         return f(x + 2, y) + f(x + 5, y)

# print(f(1, 18))



