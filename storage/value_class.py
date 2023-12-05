class Value_page():

    def __init__(self):
        self.korzina_len = 0
        self.list_korzina = []


    def add_korzina_product(self, product):
        self.korzina_len += 1
        self.list_korzina.append(product)


    def sort_list_korzina(self, sort):
        if sort == 'Названию':
            new_list = []
            nazv = []
            for i in self.list_korzina:
                nazv.append(i.name.content.content.value)
            nazv.sort()
            for i in nazv:
                for j in self.list_korzina:
                    if j.name.content.content.value == i:
                        new_list.append(j)
                        self.list_korzina.remove(j)
                        break
            self.list_korzina = new_list.copy()
        elif sort == 'Магазин КБ':
            new_list = []
            nazv = []
            for i in self.list_korzina:
                if len(i.shops.content.content.controls) > 1:
                    continue
                else:
                    nazv.append(i.shops.content.content.controls[0].controls[1].value)
            nazv.sort(reverse=True)
            for i in nazv:
                for j in self.list_korzina:
                    if len(j.shops.content.content.controls) > 1:
                        continue
                    if j.shops.content.content.controls[0].controls[1].value == i:
                        new_list.append(j)
                        self.list_korzina.remove(j)
                        break
            self.list_korzina = new_list.copy()
        elif sort == 'Магазин Бристоль':
            new_list = []
            nazv = []
            for i in self.list_korzina:
                if len(i.shops.content.content.controls) > 1:
                    continue
                else:
                    nazv.append(i.shops.content.content.controls[0].controls[1].value)
            nazv.sort()
            for i in nazv:
                for j in self.list_korzina:
                    if len(j.shops.content.content.controls) > 1:
                        continue
                    if j.shops.content.content.controls[0].controls[1].value == i:
                        new_list.append(j)
                        self.list_korzina.remove(j)
                        break
            self.list_korzina = new_list.copy()
        elif sort == 'Минимальной цене':
            new_list = []
            nazv = []
            for i in self.list_korzina:
                nazv.append(float(i.price.content.content.value.replace(' ₽', '').split(' - ')[0]))
            nazv.sort()
            for i in nazv:
                for j in self.list_korzina:
                    if float(j.price.content.content.value.replace(' ₽', '').split(' - ')[0]) == i:
                        new_list.append(j)
                        self.list_korzina.remove(j)
                        break
            self.list_korzina = new_list.copy()
        elif sort == 'Максимальной цене':
            new_list = []
            nazv = []
            for i in self.list_korzina:
                nazv.append(float(i.price.content.content.value.replace(' ₽', '').split(' - ')[1]))
            nazv.sort(reverse=True)
            for i in nazv:
                for j in self.list_korzina:
                    if float(j.price.content.content.value.replace(' ₽', '').split(' - ')[1]) == i:
                        new_list.append(j)
                        self.list_korzina.remove(j)
                        break
            self.list_korzina = new_list.copy()
        # for i in self.list_korzina:
            


    def delete_korzina_product(self, product):
        self.korzina_len -= 1
        self.list_korzina.remove(product)


class Product():

    def __init__(self, name, info, count, image, shops, price, max_count):
        self.name = name
        self.info = info
        self.count = count
        self.image = image
        self.shops = shops
        self.price = price
        self.max_count = max_count
    


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



