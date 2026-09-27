import joblib  # Библиотека для сохранения модели в бинарный файл
import pandas as pd
from sklearn.model_selection import train_test_split  # Импорт функции для разделения выборки
from sklearn.linear_model import LogisticRegression  # Модель - логистическая регрессия
from sklearn.metrics import precision_score, recall_score  # Метрики


data = pd.read_csv("fastapi/guide/data/scoring.csv")

X = data.drop(columns=["default"]).values
y = data["default"]

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)  # 80% выборки для обучения

# Инициализация модели и class_weight="balanced" - увеличение штрафа
# за неверную классификацию клиентов с дефолтом примерно в 10 раз
model = LogisticRegression(class_weight="balanced")
model.fit(X_train, y_train)

y_hat = model.predict(X_val)
precision = precision_score(y_val, y_hat)
recall = recall_score(y_val, y_hat)

print(f"Отказано: {y_hat.mean() * 100:.0f}%")  # Модель будет отклонять столько процентов заявок
print(f"Точность: {precision * 100:.0f}%")  # Заявки, по которым модель предсказывает дефолт, реально закончатся дефолтом
print(f"Полнота:  {recall * 100:.0f}%")  # С такой полнотой модель позволит выявить заявки клиентов с будущим дефолтом

joblib.dump(model, "fastapi/guide/model.pkl")
