import time

start: time = time.time()
from calculate_distance import calculate_for_user, get_addresses_shops

print(calculate_for_user(user_address="Владимир ул. Нижняя Дуброва, 17", shop_address="Владим. обл. г.Владимир ул.Гастелло д.1", flag="walk"))
print(f"run ---- {time.time() - start} sec")

print(get_addresses_shops())



