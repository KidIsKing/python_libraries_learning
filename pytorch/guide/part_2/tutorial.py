import torch


# Тензоры
a = torch.tensor([1, 2, 3])
b = torch.tensor([1.2, 3.6, 2.4])
c = a * 3
d = b ** 2
e = a + b

print(a, b, c, d, e)
print(b.mean(), b.std())  # Среднее и стандартное отклонение
# Невозможно найти среднее по тензору целых чисел.

error = (a - b) ** 2
print(error.mean())  # Средний квадрат отклонения


a = torch.tensor([[0.4, 1.8], [0.1, 1.4]])
b = torch.tensor([[0.6, 1.2], [0.9, 1.6]])
c = 2 * (a + b)
d = a @ b  # Матричное произведение

print(a, b, c, d)

print(a.mean())
print(a.mean(0))  # "Сворачиваем все строки" и получаем среднее в каждой колонке, передав порядок "сворачиваемой" оси
print(a.mean(1))


# Подготовка данных
# Разбиение и нормализация
data = torch.tensor([
    [0.076, 34.0, 5.0],
    [0.098, 67.0, 5.0],
    [0.092, 54.0, 5.0],
    [0.075, 60.0, 6.0]
])
index = [3, 2, 1, 0]
print(data[3])
print(data[index])  # Вывод матрицы в обратном порядке


index = torch.randperm(4)  # Индексы от 0 до 1 в рандомной последовательности
print(index)  # tensor([0, 1, 3, 2])
data = data[index]  # Случайно перемешаем строки исходной матрицы
print(data)

train_data, val_data = data[:2], data[2:]
print(train_data, val_data)

X_train, y_train = train_data[:, :-1], train_data[:, -1:]  # Разделяем признаки и истинные значения
print(X_train, y_train)

# Посчитаем нужные значения в каждой колонке
mean = data.mean(0)
std = data.std(0)
print(mean, std)

data = (data - mean) / std  # Нормализация
print(data)  # data * std + mean - обратная операция
