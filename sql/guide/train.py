import pandas as pd
from catboost import CatBoostRegressor  # Модель регрессии
from sklearn.metrics import mean_absolute_percentage_error  # Метрика (средний процент отклонения)


# До объединения таблиц: "Ошибка на тестовой выборке: 30.3%" - это
# значит, что модель ошибается в 30% случаев.
# После объединения таблиц: "Ошибка на тестовой выборке: 23.0%". Успех!
# Без объединения модель не учитывала тип магазина и усредняла выручку.

train_data = pd.read_csv("sql/guide/data/new_train.csv")
test_data = pd.read_csv("sql/guide/data/new_test.csv")

X_train = train_data.drop(columns=["amount"])  # Колонку с выручкой убираем
y_train = train_data["amount"]  # Предсказание модели
X_test = test_data.drop(columns=["amount"])
y_test = test_data["amount"]

model = CatBoostRegressor(cat_features=["store_type", "assortment"])
model.fit(X_train, y_train)

score = mean_absolute_percentage_error(y_test, model.predict(X_test))
print(f"Ошибка на тестовой выборке: {100 * score:.1f}%")
