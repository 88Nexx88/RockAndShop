import os.path
import sqlite3


def get_name_products():
    with sqlite3.connect('db.db3') as conn:
        return [i[0] for i in conn.cursor().execute("SELECT name FROM unique_products").fetchall()]

def search_products(search_query, database_file='db.db3'):
    try:
        with sqlite3.connect(database_file) as conn:
            cursor = conn.cursor()

            # Разбиваем входной запрос на отдельные слова
            search_terms = search_query.split()

            # Создаем список для хранения результатов поиска
            results = []

            # Создаем SQL-запрос с условиями LIKE для каждого слова в запросе
            sql_query = "SELECT name, address, pic_url, price, name_shop FROM unique_products WHERE "
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

        return {i: {'name': unique_results[i][0],
                        'address': unique_results[i][1].split("|"),
                        'pic_url': unique_results[i][2],
                        'price': unique_results[i][3],
                        'name_shop': unique_results[i][4]
                    } for i in range (len(unique_results))}
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении поиска: {e}")
        return None

res = search_products(input("Введите название продукта: "))
for i in res:
    print(f"---- {i} ----  \n {res[i]['name']}\n{res[i]['address']}\n{res[i]['pic_url']}\n{res[i]['price']}\n{res[i]['name_shop']}")
    print(os.path.exists(f'{res[i]["pic_url"]}'))
