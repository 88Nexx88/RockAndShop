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

    def __init__(self, name, info, count, image):
        self.name = name
        self.info = info
        self.count = count
        self.image = image

    