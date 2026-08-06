import torch
# Импортируем линейный слой, функции активации и класс для объединения слоёв
from torch.nn import Linear, ReLU, Sigmoid, Softmax, Sequential, MSELoss, BCELoss, CrossEntropyLoss


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
