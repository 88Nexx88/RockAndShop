import time
import sqlite3
from io import BytesIO
import tqdm
import pandas as pd
import os

from PIL import Image
from pandas import DataFrame

def sql_executor(sql_query: str):
    with sqlite3.connect('db.db3') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        return cursor.execute(sql_query)
def create_correct_name(name: str) -> str:
    # Формирование корректного имени для поиска в директории с картинками, обработка спецсимволов
    return name.split('\n')[0].replace('/', "").replace(".", "").replace('-',"").replace("%", '').replace(",", '').replace("+", "").replace("'", "").replace("&", "").replace("(", "").replace(")", "")
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
        "name_shop": []
    }

    main_df: DataFrame = pd.concat([pd.read_csv(
        f'{csv_directory}{csv}',
        usecols=['name', 'price', 'pic_url', 'address', 'name_shop'])
        for csv in [f for f in os.listdir(csv_directory) if f.endswith('.csv')]], ignore_index=True)
    main_df.dropna(inplace=True)

    # print(len(set(main_df["name"].tolist())))
    for name in tqdm.tqdm(list(set(main_df["name"].tolist())), desc="Processing...", ncols=200):
        # получение цены товара из DF со всеми товарами
        price_value = main_df.loc[main_df["name"] == name, "price"].iloc[0]

        # Получение адресов магазинов, в которых текущий товар в наличии
        address_values = "|".join(set(main_df.loc[main_df["name"] == name, "address"].tolist()))

        # Заполняем данные для нового DataFrame
        dict_of_data["name"].append(name)
        dict_of_data["price"].append(price_value)
        # Заполнение БД картинками в бинарном виде
        dict_of_data["pic_url"].append(find_image_product(name))
        dict_of_data["address"].append(address_values)
        dict_of_data["name_shop"].append(main_df.loc[main_df["name"] == name, "name_shop"].iloc[0])


    # Формирование финального DF для помещения в БД
    with sqlite3.connect(database) as conn:
        DataFrame(dict_of_data).to_sql("unique_products", conn, if_exists='replace', index=False,
                        dtype={'name': 'TEXT', 'address': 'TEXT', 'name_shop': 'TEXT', 'price': 'TEXT',
                               'pic_url': 'TEXT'})
        conn.cursor().execute('DELETE from unique_products WHERE pic_url LIKE "%error%"')
def drop_all_tables(database_file):
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