import torch


X_train = torch.load("pytorch/guide/part_2/data/X_train.pt")
y_train = torch.load("pytorch/guide/part_2/data/y_train.pt")
X_val = torch.load("pytorch/guide/part_2/data/X_val.pt")
y_val = torch.load("pytorch/guide/part_2/data/y_val.pt")

W = torch.randn(11, 1, requires_grad=True)  # Генерация случайных тензоров для таблицы весов
b = torch.randn(1, requires_grad=True)  # Аналогично для матрицы векторов смещений

# y_hat = X_train @ W + b

# Размерности совпадают
# print(y_hat.shape)
# print(y_train.shape)

# Функция потерь вычисляется без ошибок
# loss = ((y_hat - y_train) ** 2).mean()
# print(loss)  # 38.8131

alpha = 0.01

for _ in range(1000):
    y_hat = X_train @ W + b
    loss = ((y_hat - y_train) ** 2).mean()
    loss.backward()
    with torch.no_grad():
        W -= alpha * W.grad
        b -= alpha * b.grad
    W.grad = None
    b.grad = None
    print(f"Ошибка: {loss:.2f}.")

with torch.no_grad():
    y_hat = X_val @ W + b
score = (y_hat - y_val).abs().mean()
print(f"Среднее отклонение: {score:.2f} балла.")
