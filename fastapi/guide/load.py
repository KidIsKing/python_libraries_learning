"""TODO: csv файл с этими признаками: возраст, наличие образования, автомобиля, постоянной работы и уровень дохода
Источник данных и их описание: https://www.kaggle.com/competitions/fintech-credit-scoring/data.
Учесть отсутствие данных в таблице и удалить записи с пропусками перед тем, как менять значения в них.
"""

import pandas as pd


data = pd.read_csv("fastapi/guide/data/application_info.csv")
default_data = pd.read_csv("fastapi/guide/data/default_flg.csv")

# Оставляем только нужные колонки
data = data[["age", "income", "education_cd", "good_work_flg", "car_own_flg"]]
data["default"] = default_data["default_flg"]  # И добавляем результаты: да или нет дефолт
data.rename(columns={
    "income": "salary",
    "education_cd": "education",
    "good_work_flg": "work",
    "car_own_flg": "car",
}, inplace=True)

# Меняем образование на флаг наличия высшего образования
# print(data.education.unique())  # Вывод уникальных значений в колонке education
education_Y = ["GRD", "PGR", "ACD"]  # Да, несколько или учёная степень
data["education"] = data["education"].apply(lambda x: 1 if x in education_Y else 0)
# Меняем обозначения Y и N на 0 и 1 для наличия автомобиля
data["car"] = data["car"].apply(lambda x: 1 if x == "Y" else 0)
# Меняем дробное число на целое в колонке дефолта
# data["default"] = data["default"].astype("Int32")
data["default"] = data["default"].apply(lambda x: 1 if x == 1.0 else 0)
# Зарплата будет указана в тысячах рублей
data["salary"] = data["salary"] // 1000

# Перемешиваем данные
data = data.sample(frac=1, random_state=22)  # frac=1 - перемешивание всей выборки
print(data.head())

data.to_csv("fastapi/guide/data/scoring.csv", index=False)
