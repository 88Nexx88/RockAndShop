
import sqlite3

def search_fts_table(search_term):
    with sqlite3.connect("db.db3") as conn:
        table_name = 'unique_products_fts'
        original_table_name = 'unique_products'
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS unique_products_fts')
        cursor.execute(f'''
                    CREATE VIRTUAL TABLE IF NOT EXISTS {table_name} USING fts4(name, price, pic_url, address, name_shop, count, sale, min, max, tokenize=unicode61)''')
        cursor.execute(f'''
                INSERT INTO {table_name} SELECT * FROM {original_table_name}
            ''')
        # Ищем виртуальную таблицу по столбцу name, игнорируя регистр
        results = cursor.execute(f"SELECT * FROM {table_name} WHERE name MATCH ? COLLATE NOCASE", (search_term,)).fetchall()
        unique_results = list(set(results))
        unique_results.sort()

        return {i: {'name': unique_results[i][0],
                    'price': unique_results[i][1],
                    'pic_url': unique_results[i][2],
                    'address': unique_results[i][3].split("|"),
                    'name_shop': unique_results[i][4],
                    'count': [int(i) for i in unique_results[i][5].split(",")],
                    'sale': [float(i) for i in unique_results[i][6].split(",")],
                    'min': unique_results[i][7],
                    'max': unique_results[i][8]
                    } for i in range(len(unique_results))}



res = search_fts_table(input("Введите название продукта: "))
for i in res:
    print(f"---- {i} ----  \n {res[i]['name']}\n{res[i]['address']}\n{res[i]['pic_url']}\n{res[i]['price']}\n{res[i]['name_shop']}\n"
          f"{res[i]['count']}\n{res[i]['sale']}\n{res[i]['min']}\n{res[i]['max']}")
def get_products_all(names_products: list):
    with sqlite3.connect("db.db3") as conn:
        cursor = conn.cursor()
        sql_query = "SELECT * FROM unique_products WHERE "
        sql_query += " OR ".join(["name = ?" for _ in names_products])
        unique_results = cursor.execute(sql_query, names_products).fetchall()
        # unique_results.sort()

        return {i: {'name': unique_results[i][0],
                    'price': unique_results[i][1],
                    'pic_url': unique_results[i][2],
                    'address': unique_results[i][3].split("|"),
                    'name_shop': unique_results[i][4],
                    'count': [int(i) for i in unique_results[i][5].split(",")],
                    'sale': [float(i) for i in unique_results[i][6].split(",")],
                    'min': unique_results[i][7],
                    'max': unique_results[i][8]
                    } for i in range(len(unique_results))}

temp = ['Вино игристое ЗИМОР ПРОСЕККО 8,5-13,5% БЕЛ. СУХ. 0,75Л',
                          'Пиво имп. CERNA KRALOVNA SVETLY LEZAK СВЕТЛ. ФИЛЬТР. ПАСТЕР. Ж/Б. 0,5Л',
                    'Вино игристое Мондоро Асти защ.наим.DOCG Пьемонт белое сладкое\nИталия, 0.75 л., Пьемонт, 7.5%',
                    'Сок ДОБРЫЙ ЯБЛОКО 2Л', 'Мармелад жевательный MAMBA ФРУМЕЛАДКИ МОЛОЧНЫЕ ПРИВИДЕНИЯ 90Г',
                    'Вино Шато Тамань Пино Гриджио белое сухое\nРоссия, 0.75 л., Кубань, 12%',
                    'Вино сортовое ординарное РОШ МАЗЕ МУСКАТ МУАЛЛЕ 8,5-15% БЕЛ. П/СЛ 0,75Л',
                    'Набор конфет Черриссимо Классик\nПольша, 142 г']



# res = get_products_final(temp)
#
# for i in res:
#     print(f"---- {i} ----  \n {res[i]['name']}\n{res[i]['address']}\n{res[i]['pic_url']}\n{res[i]['price']}\n{res[i]['name_shop']}\n"
#           f"{res[i]['count']}\n{res[i]['sale']}\n{res[i]['min']}\n{res[i]['max']}")
# print(len(temp))


def get_one_products(name: str) -> dict:
    with sqlite3.connect("db.db3") as conn:
        cursor = conn.cursor()
        unique_results = cursor.execute(f"SELECT * FROM unique_products WHERE name IS ?", (name,)).fetchall()
        return {i: {'name': unique_results[i][0],
                    'price': unique_results[i][1],
                    'pic_url': unique_results[i][2],
                    'address': unique_results[i][3].split("|"),
                    'name_shop': unique_results[i][4],
                    'count': [int(i) for i in unique_results[i][5].split(",")],
                    'sale': [float(i) for i in unique_results[i][6].split(",")],
                    'min': unique_results[i][7],
                    'max': unique_results[i][8]
                    } for i in range(len(unique_results))}


# print(get_one_products('Устройство IQOS 3 DUOS ЧЕРНЫЙ'))