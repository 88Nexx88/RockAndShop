import time
import sqlite3
import pandas as pd
import os

def from_csv_to_database(db_file: str, csv_folder: str, shop_flag: str):
    with sqlite3.connect(db_file) as conn:
        # Получение списка CSV-файлов в папке
        csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

        # Цикл для обработки каждого CSV-файла
        for csv_file in csv_files:
            # Имя таблицы будет таким же, как имя файла без расширения .csv
            match shop_flag:
                case "kb":
                    table_name = "kb_"+os.path.splitext(csv_file)[0]
                case "bristol":
                    table_name = "bristol_" + os.path.splitext(csv_file)[0]

            # Чтение CSV-файла в Pandas DataFrame
            df = pd.read_csv(os.path.join(csv_folder, csv_file))
            # Сохранение DataFrame в базе данных SQLite
            df.to_sql(table_name, conn, if_exists='replace', index=False)


def get_names_tables(flag: str = 'all'):
    match flag:
        case "all":
            with sqlite3.connect('db.db3') as conn:
                cursor = conn.cursor()
                return [i[0] for i in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name != 'unique_products'").fetchall()]
        case "kb":
            with sqlite3.connect('db.db3') as conn:
                cursor = conn.cursor()
                return [i[0] for i in cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'kb_%'").fetchall()]
        case "bristol":
            with sqlite3.connect('db.db3') as conn:
                cursor = conn.cursor()
                return [i[0] for i in cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table' AND name name LIKE 'bristol_%'").fetchall()]

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

def get_name_products():
    with sqlite3.connect('db.db3') as conn:
        return [i[0] for i in conn.cursor().execute("SELECT name FROM unique_products").fetchall()]

def generate_sql(flag: str, name_product: str):
    with sqlite3.connect('db.db3') as conn:
        cursor = conn.cursor()
        temp: int = 1
        tables = get_names_tables("all")

        sql: str = ""
        for table in tables:
            if temp < len(tables):
                try:
                    sql += f"SELECT address FROM `{table}` WHERE name = '{name_product}' UNION "
                except sqlite3.OperationalError:
                    sql += f'SELECT address FROM `{table}` WHERE name = "{name_product}" UNION '
                finally:
                    temp += 1
            else:
                try:
                    sql += f"SELECT address FROM `{table}` WHERE name = '{name_product}'"
                except sqlite3.OperationalError:
                    sql += f'SELECT address FROM `{table}` WHERE name = "{name_product}"'
                finally:
                    temp += 1
    return sql

def create_dict_product_address():
    with sqlite3.connect('db.db3') as conn:
        cursor = conn.cursor()
        dict_of_products_query: dict = {}
        products: list = get_name_products()
        for product in products:
            dict_of_products_query[product] = generate_sql('for_search', product)
            print(f"{product} -- {dict_of_products_query[product]}")

        for product in dict_of_products_query:
            try:
                dict_of_products_query[product] = [i[0] for i in cursor.execute(dict_of_products_query[product]).fetchall()]
            except sqlite3.OperationalError:
                print(f"Error, {product}")
        print(len(dict_of_products_query))
        for i in dict_of_products_query:
            print(f"{i} --- {dict_of_products_query[i]}")
            break


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
        tables = get_names_tables('all')

        # Цикл для обработки каждой таблицы
        for table in tables:
            print(table)
        if "kb_" in table:
            cursor.execute(
                f"INSERT OR IGNORE INTO unique_products (pic_url, name_shop, name) SELECT DISTINCT id, pic_url, name_shop, name FROM `{table}`")
        # else:
        #     cursor.execute(
        #         f"INSERT OR IGNORE INTO unique_products (pic_url-src, pic_url_slide-src,, name) SELECT DISTINCT id, pic_url, name_shop, name FROM `{table}`")






if __name__ == "__main__":
    start = time.time()
    create_dict_product_address()
    print(f"running time - {(time.time() - start)/60} min")