import torch
# Импортируем линейный слой, функции активации и класс для объединения слоёв
from torch.nn import Linear, ReLU, Sigmoid, Softmax, Sequential, MSELoss, BCELoss, CrossEntropyLoss
from torch.optim import SGD  # Stochastic Gradient Descent


X = torch.tensor([[0.4, 0.5], [0.9, 0.2], [0.2, 0.0], [0.1, 0.0]])
# W = torch.tensor([[0.2, 0.5, 1.0], [0.7, 0.4, 0.4]])

# print(X, W, sep="\n")
# # print(X * W)  # Поэлементное умножение матриц, где размерности должны совпадать
# print(X @ W)

# Не создаём матрицу весов, а создаём линейных слой
linear = Linear(2, 3)  # Количество слоёв на входе и на выходе
# print(linear.weight)  # Матрица 2 на 3, заполненная случайными числами
print(linear(X))  # Применяем линейных слой к матрице X


X = torch.tensor([[0.4, -0.5, 0.9], [0.3, 0.2, -0.1], [0.1, 0.7, -0.2]])
linear = ReLU()  # max(0, x)
print(X)
print(linear(X))

X = torch.tensor([[6.7], [-3.2], [1.1]])
linear = Sigmoid()
print(X)
print(linear(X))

X = torch.tensor([[0.4, -0.5, 0.9], [0.3, 0.2, -0.1], [0.1, 0.7, -0.2]])
linear = Softmax()
print(X)
print(linear(X))

X = torch.tensor([[0.4, -0.5, 0.9], [0.3, 0.2, -0.1], [0.1, 0.7, -0.2]])
model = Sequential(  # Модель для регрессии
    Linear(3, 10),  # 3 входных слоя, 10 признаков на выходе
    ReLU(),
    Linear(10, 20),  # Пересчитаем 10 признаков в 20
    ReLU(),
    Linear(20, 1)  # 20 признаков в ответ
)
# Если решаем более сложную задачу, нужно добавить в конец ещё слой
# активации Sigmoid или Softmax и при необходимости изменить количество
# признаков в последнем слое.
print(model(X))  # Получаем предсказание модели

# Практика 1
model = Sequential(
    Linear(3, 16),
    ReLU(),
    Linear(16, 32),
    ReLU(),
    Linear(32, 5),
    Softmax()
)
print(model(X))

model = Sequential(
    Linear(3, 32),
    ReLU(),
    Linear(32, 32),
    ReLU(),
    Linear(32, 1),
)
print(model(X))

model = Sequential(
    Linear(3, 16),
    ReLU(),
    Linear(16, 1),
    Sigmoid()
)
print(model(X))


loss_fn = MSELoss()
y = torch.tensor([[0.5], [1.5], [0.7]])
y_hat = torch.tensor([[0.6], [0.2], [0.5]])
print(loss_fn(y_hat, y))  # Аргументы передаём обязательно в таком порядке

loss_fn = BCELoss()
y = torch.tensor([[1.0], [1.0], [0.0]])
y_hat = torch.tensor([[0.9], [0.3], [0.2]])
print(loss_fn(y_hat, y))

loss_fn = CrossEntropyLoss()
y = torch.tensor([1, 2, 0])
y_hat = torch.tensor([
    [-1.2, 2.2, 0.2],
    [2.3, 0.2, 0.7],
    [0.9, -2.2, -1.2]
])  # Ожидается, что последним слоём будет линейный слой (Softmax под капотом)
print(loss_fn(y_hat, y))


# Подсчёт средний процент отклонения
y = torch.tensor([[0.5], [1.5], [0.7]])
y_hat = torch.tensor([[0.6], [0.2], [0.5]])
score = (y_hat - y).abs() / y * 100
# Если в значениях есть нули, то в результате будет или очень большое число, или неопределённость
print(score.mean())

# Точность предсказаний модели для бинарной классификации
y = torch.tensor([[1.0], [1.0], [0.0]])
y_hat = torch.tensor([[0.9], [0.3], [0.2]])
score = (y_hat.round() == y).sum() / len(y) * 100
# Если в значениях есть нули, то в результате будет или очень большое число, или неопределённость
print(score)  # Получаем процент объектов, которые модель верно классифицировала

# Мультиклассовая классификация
y = torch.tensor([1, 2, 0])
y_hat = torch.tensor([
    [-1.2, 2.2, 0.2],
    [2.3, 0.2, 0.7],
    [0.9, -2.2, -1.2]
])
# .argmax() для каждой строки возвращает номер колонки с наибольшим значением
score = (y_hat.argmax(1) == y).sum() / len(y) * 100
print(score)


# Обучение нейросети. Для обучения используем игрушечный набор данных iris.
# Задача заключается в том, чтобы по параметрам цветка определить,
# к какому из трех сортов ириса он относится. То есть, это
# задача мультиклассовой классификации. Параметров всего 4 — длина и ширина
# чашелистика (sepal) и длина и ширина лепестка (petal).
X = torch.load("D:/Dev/Learning/python_libraries_learning/pytorch/guide/data/data.pt")
y = torch.load("D:/Dev/Learning/python_libraries_learning/pytorch/guide/data/target.pt")
print(X[:3], y[:3])
print(len(X))  # 150 объектов
# 100 объектов на обучение, 50 - на валидацию
# Ещё обычно их нужно перемешивать, но данные уже перемешаны
X_train, X_val = X[:100], X[100:]
y_train, y_val = y[:100], y[100:]

model = Sequential(Linear(4, 16), ReLU(), Linear(16, 3))
loss_fn = CrossEntropyLoss()
# y_hat = model(X_train)  # Предсказание модели
# loss = loss_fn(y_hat, y_train)  # Величина функции потерь
# print(y_hat, loss)  # Значения на данном этапе не важны

# Реализация градиентного спуска
# gradient = loss.backward()  # Частные производные функции потерь по параметрам модели / градиент
# print(gradient)  # Получаем None, потому что в PyTorch вместо явного возврата
# производных, результаты записываются прямо в те матрицы, которые
# использовались в вычислениях, в данном случае, в веса модели.

print(model[0].weight)  # requires_grad=True
print(model[0].weight.grad)  # None, если вызов backward() убрать, в противном
# случае - выводится матрица, где в каждой ячейке находится частная
# производная по соответствующему параметру.

# loss.backward()
# print(loss)  # Посмотрим на значения функции потерь до градиентного спуска
# Градиентный спуск вручную, который выдаст ошибку:
# alpha = 0.01
# model[0].weight -= alpha * model[0].weight.grad
# model[2].weight -= alpha * model[2].weight.grad
# Воспользуемся встроенным оптимизатором:
# В аргументах: веса модели, которыми оптимизатор будет управлять и величина коэффициента обучения
optimizer = SGD(model.parameters(), lr=0.01)
# optimizer.step()  # Обновление весов
# print(loss_fn(model(X_train), y_train))  # И после алгоритма значения стали меньше

# Операцию оптимизации нужно выполнить много раз для большей гарантии получения точки минимума
for _ in range(100):
    y_hat = model(X_train)
    loss = loss_fn(y_hat, y_train)
    loss.backward()  # Каждый новый вызов не заменяет производные, а суммирует их значения с предыдущеми - ошибка
    optimizer.step()
    optimizer.zero_grad()  # Обнуление всех производных, чтобы избавиться от суммирования (сотрёт память модели о предыдущих итерациях)
    print(f"{loss:0.3f}")  # Значение функции потерь стабильно падает!

score = (model(X_val).argmax(1) == y_val).sum() / len(y_val) * 100
print(f"Точность модели: {score}%")  # Сколько процентов объектов, классы которых были верно предсказаны
# Поскольку выборка очень маленькая, точность будет разной, так как существенное влияние имеет случайная инициализация