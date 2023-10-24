"""
Должна быть какая-то общая таблица, где будут перечислены все уникальные продукты из всех других таблиц.
Именно при помощи этой таблицы будет работать поиск в самой ИАС. Должна быть реализована связь один к одному
(продукта из общей таблицы к продукту из таблицы магазина), если продукт уникальный и содержится только в одном магазине.
Также может быть реализована связь один ко многим, если конкретный продукт из общей таблицы содержится в нескольких магазинах.
Именно на эти продукты из других магазинов и должен ссылаться продукт из общей таблицы, если он был выбран пользователем ИАС.
Нужно реализовать правильный поиск по БД, чтобы при введении нескольких символов пользователем ему выдавалось уже
какое-то количество названий продуктов, которые начинаются на эти же символы (используя регулярки, наверное).



При поисковом запросе пользователю должен выдаваться список со следующей инфорамцией:
имя товара, мини-информация о нем?, количество товара?, картинка товара, наличие в кб, наличие в пятерке.



Нужно долеать вставку картинок в pic_url, так как название фалов png не соответсвуют названиям продуктов.
"""

import time
import pandas as pd
import sqlite3
import os
from PIL import Image
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


def create_unique_table(db_file: str):
    # Подключение к базе данных SQLite
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        # Создаем новую таблицу для хранения уникальных продуктов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS unique_products (
                id INTEGER PRIMARY KEY,
                pic_url BLOB,
                name_shop TEXT,
                name TEXT NOT NULL,
                UNIQUE (name)
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
                cursor.execute(
                    f"INSERT OR IGNORE INTO unique_products (id, pic_url, name_shop, name) SELECT DISTINCT id, pic_url, name_shop, name FROM `{table_name}`")


def add_foreign_keys(db_file: str):
    """
    После вормирования таблицы unique_products создает новые таблицы конкретных магазинов, перенося данные из старых, это делается
    для добавления внешего ключа id, чтобы каждый продукт из конкретного магазина ссылался на продукт из таблицы unique_products.
    Затем, удаляет старые таблицы.... Костыли, ну а что поделать.........................
    """

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'unique_products';")
        tables = cursor.fetchall()

        # Создание новых таблиц, перенос данных и установка внешних ключей
        for table in tables:
            table_name = table[0]

            # Получение схемы существующей таблицы
            cursor.execute(f"PRAGMA table_info(`{table_name}`);")
            table_schema = cursor.fetchall()

            # Итеративно генерируем SQL для создания новой таблицы с внешним ключом
            create_table_sql = f'CREATE TABLE IF NOT EXISTS `kb_{table_name}` (\n'
            for column in table_schema:
                column_name = column[1]
                column_type = column[2]
                if column_name == "pic_url":
                    create_table_sql += f'"{column_name}" BLOB,\n'
                else:
                    create_table_sql += f'"{column_name}" {column_type},\n'
            create_table_sql += 'FOREIGN KEY ("id") REFERENCES unique_products("id")\n);'

            # Создаем новую таблицу
            cursor.execute(create_table_sql)

            # Переносим данные из старой таблицы в новую
            cursor.execute(f'INSERT INTO `kb_{table_name}` SELECT * FROM `{table_name}`;')

            # Удаляем старую таблицу
            cursor.execute(f'DROP TABLE IF EXISTS `{table_name}`;')

def update_pic_url(db_file: str):
    with sqlite3.connect(db_file) as conn:

        cursor = conn.cursor()

        # Получаем список всех таблиц в базе данных
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Директория с изображениями товаров
        image_dir = '/home/valery/Рабочий стол/IAS/IAS_Rock_and_shop/code/Shops/KB/img'

        # Цикл для обработки каждой таблицы
        for table in tables:
            table_name = table[0]

            # Получаем данные из столбца 'name' и 'pic_url' для каждой строки в таблице
            cursor.execute(f'SELECT name, pic_url FROM `{table_name}`')
            rows = cursor.fetchall()

            # Обновляем столбец 'pic_url' для каждой строки
            for row in rows:
                product_name = row[0]
                pic_url = f'{image_dir}/{product_name}.png'  # Формируем путь к изображению
                print(pic_url)
                # Проверяем, существует ли файл с изображением
                if os.path.exists(pic_url):
                    print("Rock")
                    # Открываем изображение и сохраняем его в столбец 'pic_url'
                    with open(pic_url, 'rb') as image_file:
                        image_data = image_file.read()
                        cursor.execute(f"UPDATE `{table_name}` SET pic_url = ? WHERE name = ?",
                                       (sqlite3.Binary(image_data), product_name))


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


def search_products(search_query, database_file):
    try:
        with sqlite3.connect(database_file) as conn:
            cursor = conn.cursor()

            # Разбиваем входной запрос на отдельные слова
            search_terms = search_query.split()

            # Создаем список для хранения результатов поиска
            results = []

            # Создаем SQL-запрос с условиями LIKE для каждого слова в запросе
            sql_query = "SELECT name FROM unique_products WHERE "
            sql_conditions = []
            for term in search_terms:
                sql_conditions.append("name LIKE ?")
            sql_query += " AND ".join(sql_conditions)

            # Выполняем SQL-запрос
            cursor.execute(sql_query, ['%' + term + '%' for term in search_terms])
            term_results = cursor.fetchall()
            results.extend(term_results)

        # Убираем дубликаты и сортируем результаты
        unique_results = list(set(results))
        unique_results.sort()

        return unique_results
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении поиска: {e}")
        return None


# Пример использования функции


if __name__ == "__main__":
    db_file = "db.db3"
    csv_folder = "Shops/KB"
    kb_img_folder: str = "Shops/KB/img"
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
                add_foreign_keys(db_file)
            case 3:
                drop_all_tables(db_file)
            case 4:
                search_term = input("\n\nКакой продукт ищете?: ")
                results = search_products(search_term, db_file)

                print(type(results))
                if results:
                    print("Результаты поиска:")
                    for row in results:
                        all = row[0].split("\n", 1)
                        print(f"--- {all[0]} ---")
                    print(f"!!!!!! Количество результатов поиска: {len(results)} !!!!!")
                else:
                    print("Ничего не найдено.")
            case 5:
                drop_all_tables(db_file)
                create_or_update_tables(db_file, csv_folder)
                create_unique_table(db_file)
                add_foreign_keys(db_file)
                update_pic_url(db_file)