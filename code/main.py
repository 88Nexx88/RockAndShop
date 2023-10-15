"""
Должна быть какая-то общая таблица, где будут перечислены все уникальные продукты из всех других таблиц.
Именно при помощи этой таблицы будет работать поиск в самой ИАС. Должна быть реализована связь один к одному
(продукта из общей таблицы к продукту из таблицы магазина), если продукт уникальный и содержится только в одном магазине.
Также может быть реализована связь один ко многим, если конкретный продукт из общей таблицы содержится в нескольких магазинах.
Именно на эти продукты из других магазинов и должен ссылаться продукт из общей таблицы, если он был выбран пользователем ИАС.
Нужно реализовать правильный поиск по БД, чтобы при введении нескольких символов пользователем ему выдавалось уже
какое-то количество названий продуктов, которые начинаются на эти же символы (используя регулярки, наверное).



"""


import time
import pandas as pd
import sqlite3
import os

start = time.time()



def create_or_update_tables(db_file: str, csv_folder: str):

    # Подключение к базе данных SQLite
    with sqlite3.connect(db_file) as conn:
        # Получение списка CSV-файлов в папке
        csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

        # Цикл для обработки каждого CSV-файла
        for csv_file in csv_files:
            # Имя таблицы будет таким же, как имя файла без расширения .csv
            table_name = os.path.splitext(csv_file)[0]

            # Чтение CSV-файла в Pandas DataFrame
            df = pd.read_csv(os.path.join(csv_folder, csv_file))

            # Сохранение DataFrame в базе данных SQLite
            df.to_sql(table_name, conn, if_exists='replace', index=False)

"""---------------------------------------------------------"""

def create_unique_table (db_file: str):
    # Подключение к базе данных SQLite
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        # Создаем новую таблицу для хранения уникальных продуктов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS unique_products (
                product_name TEXT NOT NULL,
                UNIQUE (product_name)
            )
        ''')

        # Получаем список всех таблиц в базе данных
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Цикл для обработки каждой таблицы
        for table in tables:
            table_name = table[0]
            print(table_name)
            if table_name != "unique_products":
                # Извлекаем уникальные продукты из текущей таблицы и добавляем их в unique_products
                cursor.execute(f"INSERT OR IGNORE INTO unique_products (product_name) SELECT DISTINCT name FROM `{table_name}`")

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

import sqlite3

def search_products(search_term, database_file):
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # Используем оператор LIKE для поиска продуктов по введенному пользователем поисковому запросу
        cursor.execute("SELECT product_name FROM unique_products WHERE product_name LIKE ?", ('%' + search_term + '%',))
        result = cursor.fetchall()

        # Закрываем соединение
        conn.close()

        return result
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении поиска: {e}")
        return None




if __name__ == "__main__":
    db_file = "/home/valery/Рабочий стол/IAS/db.db3"
    csv_folder = "/home/valery/Рабочий стол/IAS/Адреса"
    while True:
        question = int(input("\n\n\n\nЗавершить работу? - 0, \n"
                             "Хотите заполнить таблицу данными из csv файлов? - 1\n"
                             "Cформировать уникальную таблицу с названием продуктов? - 2, \n"
                             "Удалить все таблицы - 3, \n"
                             "Выполнить поиск - 4, \n"
                             ""
                             "---------------------------  "))
        if question == 0:
            break
        match question:
            case 1:
                create_or_update_tables(db_file, csv_folder)
            case 2:
                create_unique_table(db_file)
            case 3:
                drop_all_tables(db_file)
            case 4:
                search_term = input("\n\nКакой продукт ищете?: ")
                results = search_products(search_term, db_file)

                print(type(results))
                if results:
                    print("Результаты поиска:")
                    for row in results:
                        print(f"--- {row[0]} ---")
                    print(f"!!!!!! Количество результатов поиска: {len(results)} !!!!!")
                else:
                    print("Ничего не найдено.")


