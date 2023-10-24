
import time
import os
import shutil
import sqlite3



def get_address_from_txt():
    file_path = "/home/valery/Рабочий стол/IAS/IAS_Rock_and_shop/Shops/5ka/address"
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Разделение строки по символам табуляции и добавление ее в список
                text_list: list = line.strip().split('\t')
    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
    return list(set(text_list))

# print(get_addres_from_txt())
# counter:int = 0
# for i in get_address_from_txt():
#     print(f"{counter} --- {i}")
#     counter += 1
# address_5ka: list = get_address_from_txt()

def create_csv_address_files():
    source_file: str = "/home/valery/Рабочий стол/IAS/IAS_Rock_and_shop/Shops/5ka/out.csv"
    destination_files: list = [i+".csv" for i in get_address_from_txt()]
    for destination_file in destination_files:
        shutil.copy(source_file, f"/home/valery/Рабочий стол/IAS/IAS_Rock_and_shop/Shops/5ka/{destination_file}")

# create_csv_address_files()

# print("Вино А Мон Гран Амур белое сухое.png" in os.listdir("/home/valery/Рабочий стол/IAS/IAS_Rock_and_shop/Shops/KB/img"))

# print(os.path.abspath('Вино А Мон Гран Амур белое сухое.png'))
# -------------------------------------------- Глобальный поиск файлов по ОС -------------------------
# import os
#
# def find_file(file_name, search_directory):
#     for root, dirs, files in os.walk(search_directory):
#         if file_name in files:
#             return os.path.join(root, file_name)
#     return None  # Файл не найден
#
# # Укажите имя файла, который вы ищете, и директорию для поиска
# file_name_to_find = "sources.list"
# search_directory = "/"
# start = time.time()
# file_path = find_file(file_name_to_find, search_directory)
# if file_path:
#     print(f"Файл {file_name_to_find} найден по пути: {file_path}, {time.time() - start} sec")
#
# else:
#     print(f"Файл {file_name_to_find} не найден в директории {search_directory}, {time.time() - start} sec")
# ---------------------------------------------------------------------------------------------------------

def split_string_by_newline(input_string):
    # Разделение строки на части с помощью символа переноса строки
    parts = input_string.split('\n', 1)

    # Если найдено хотя бы две части, возвращаем первую и вторую части
    if len(parts) >= 2:
        return parts[0], parts[1]

    # Если не найдено разделителя, возвращаем всю строку и пустую строку
    return input_string, ''

# Пример использования
input_string = """Пиво Пятницкое Булгарпиво нефильтрованное ст
Россия, 0.45 л., 4.1%"""
product_name, additional_info = split_string_by_newline(input_string)
print("Название продукта:", product_name.strip())
print("Дополнительная информация:", additional_info.strip())













