import sqlite3  # Встроенная
# Вместо sqlute 3 для облачной БД
# import sqlalchemy import create_engine
import pandas as pd


# Запрос для обучения нейросети на старых данных
query_train = """
SELECT
    month,
    day_of_week,
    is_holiday,
    amount
FROM sales
WHERE date < '2025-01-01'"""

# Запрос для тестовой выборки на новых данных
query_test = """
SELECT
    month,
    day_of_week,
    is_holiday,
    amount
FROM sales
WHERE date >= '2025-01-01'"""

# Данные для обучения из объединённых таблиц
query_new_train = """
SELECT
    month,
    day_of_week,
    is_holiday,
    amount,
    store_type,
    assortment,
    competition_distance
FROM sales
JOIN stores USING(store_id)
WHERE date < '2025-01-01'"""

# Тренировочные данные из объединённых таблиц
query_new_test = """
SELECT
    month,
    day_of_week,
    is_holiday,
    amount,
    store_type,
    assortment,
    competition_distance
FROM sales
JOIN stores USING(store_id)
WHERE date >= '2025-01-01'"""

# Для работы с облачной БД вместо контекстного менеджера подключаемся через адрес
# connection = create_engine("postgresql://mouse:mouse123@5.129.250.215:5432/sales")
# ИЛИ
# connection = create_engine("sqlite://data.db")  # Если sql в облаке

with sqlite3.connect("sql/guide/data/data.db") as connection:
    data_train = pd.read_sql(query_train, connection)
    data_test = pd.read_sql(query_test, connection)
    data_new_train = pd.read_sql(query_new_train, connection)
    data_new_test = pd.read_sql(query_new_test, connection)

print(data_train.head())
print(data_train.shape)

print(data_test.head())
print(data_test.shape)


data_train.to_csv("sql/guide/data/train.csv", index=False)
data_test.to_csv("sql/guide/data/test.csv", index=False)
data_new_train.to_csv("sql/guide/data/new_train.csv", index=False)
data_new_test.to_csv("sql/guide/data/new_test.csv", index=False)

# Для работы с облачными базами данных нужно установить две библиотеки:
# sqlalchemy - универсальная библиотека для работы с sql и
# psycopg2-binary - драйвер для подключения к Postgres.
