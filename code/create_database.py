import time
import sqlite3
import tqdm
import pandas as pd
import os
import random

from pandas import DataFrame

def sql_executor(sql_query: str):
    with sqlite3.connect('db.db3') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        return cursor.execute(sql_query)
def create_correct_name(name: str) -> str:
    # Формирование корректного имени для поиска в директории с картинками, обработка спецсимволов
    return name.split('\n')[0].replace('/', "").replace(".", "").replace('-',"").replace("%", '').replace(",", '').replace("+", "").replace("'", "").replace("&", "").replace("(", "").replace(")", "")

def generate_random_counts(num_shops):
    return ','.join(str(random.randint(1, 28)) for _ in range(num_shops))

def find_image_product(name: str) -> str:
    # Проверяем, существует ли файл с изображением
    first = "Shops/All/img/" + name.split('\n')[0].replace('/', "").replace(
            ".", "").replace(
        '-',"").replace("%", '').replace(
        ",", '').replace("+", "").replace(
        "'", "").replace("&", "").replace(
        "(", "").replace(")", "")+".png"
    second = "Shops/All/img/"+name.replace("/", '-').replace("/", "-")+".png"
    if os.path.exists(first):
        return first
    elif os.path.exists(second):
        return second
    else:
        # print("################# ERROR ##############", name, first, second)
        return "error"

# Создание основной рабочей таблицы
def create_unique_table(database: str, csv_directory: str, img_directoty: str):
    dict_of_data: dict = {
        "name": [],
        "price": [],
        "pic_url": [],
        "address": [],
        "name_shop": [],
        "count": [],
        "sale": []
    }

    """Конкатенация датафреймов из csv файлов в заданной директории, 
    каждый из которых соответствует конкретному магазину неважно какой сети, используя определнные столбцы."""
    main_df: DataFrame = pd.concat([pd.read_csv(
        f'{csv_directory}{csv}',
        usecols=['name', 'price', 'pic_url', 'address', 'name_shop'])
        for csv in [f for f in os.listdir(csv_directory) if f.endswith('.csv')]], ignore_index=True)
    main_df.dropna(inplace=True)
    # Темпоральный индекс для обращения к текущей строке с адресами продукта, чтобы заполнить столбец количества товаров.
    temp_index: int = 0
    list_of_sales: list = [0, 0, 0, 0, 5, 10, 15, 20]

    for name in tqdm.tqdm(list(set(main_df["name"].tolist())), desc="Processing...", ncols=200):



        # Заполняем данные для нового DataFrame

        # Добавление имени текущего товара
        dict_of_data["name"].append(name)

        # Получение, приведение к типу float и добавление цены текущего товара с помощью методов строк
        dict_of_data["price"].append(float(main_df.loc[main_df["name"] == name, "price"].iloc[0].split(" ₽")[0].replace(" ", "")))

        # Заполнение БД картинками в бинарном виде
        dict_of_data["pic_url"].append(find_image_product(name))

        # Получение и добавление адресов магазинов, в которых текущий товар в наличии.
        # В БД будет храниться как строка из адресов магазинов с разделителем "|"
        dict_of_data["address"].append("|".join(set(main_df.loc[main_df["name"] == name, "address"].tolist())))

        # Получение и добавление имени магазина текущего товара
        dict_of_data["name_shop"].append(main_df.loc[main_df["name"] == name, "name_shop"].iloc[0])

        # Применяем функцию генерации рандомного количество товара в соответствующем магазине в диапазоне от 1 до 28
        # Будет храниться в БД в виде строки с разделителем ","
        dict_of_data['count'].append(','.join(str(random.randint(1, 28)) for _ in range(len(dict_of_data['address'][temp_index].split('|')))))
        # Рандомное генерирование величины скидки в процентах на товар в соответствующем магазине
        dict_of_data['sale'].append(','.join(str(random.choice(range(0, 21, 5))) for _ in range(len(dict_of_data['address'][temp_index].split('|')))))
        temp_index += 1



    # Формирование финального DF для помещения в БД
    with sqlite3.connect(database) as conn:
        DataFrame(dict_of_data).to_sql("unique_products", conn, if_exists='replace', index=False,
                        dtype={'name': 'TEXT', 'address': 'TEXT', 'name_shop': 'TEXT', 'price': 'REAL',
                               'pic_url': 'TEXT', "count": "TEXT", "sale": "TEXT"})

        # Удаление товаров из БД, у которых нет картинки
        conn.cursor().execute('DELETE from unique_products WHERE pic_url LIKE "%error%"')
def drop_all_tables(database_file="db.db3"):
    try:
        with sqlite3.connect(database_file) as conn:
            cursor = conn.cursor()

            # Получаем список всех таблиц в базе данных
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            # Цикл для удаления каждой таблицы
            for table in tables:
                table_name = table[0]
                cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
                print(f"Таблица {table_name} удалена.")

            print("Все таблицы удалены успешно.")
    except sqlite3.Error as e:
        print(f"Ошибка при удалении таблиц: {e}")


if __name__ == "__main__":
    start = time.time()
    create_unique_table("db.db3", "Shops/All/", "Shops/All/img/")
    # t: str = input("Введите название продукта: ")
    # # with open ('result.txt', 'w') as write_file:
    # #     write_file.write(f"{search_products(t, 'db.db3')}")
    # print(search_products(t, 'db.db3'))
    print(f"running time - {(time.time() - start) / 60 } min")
    ##### Доделать бристоль и сделать вменяемую систему предоставления результатов поиска, добавить исполнения удаления продуктов без картинки