import torch
from torch.nn import Sequential, Linear, ReLU, CrossEntropyLoss
from torch.optim import SGD


# Загрузка файлов
X = torch.load("pytorch/guide/data/data.pt")
y = torch.load("pytorch/guide/data/target.pt")

# Выборка
X_train, X_val = X[:100], X[100:]
y_train, y_val = y[:100], y[100:]

# Инициализация модели, функции потерь и оптимизатора для ГС
model = Sequential(
    Linear(4, 16),
    ReLU(),
    Linear(16, 3)
)
loss_fn = CrossEntropyLoss()
optimizer = SGD(model.parameters(), lr=0.01)

# Обучение повторением шагов градиентного спуска
for _ in range(100):
    y_hat = model(X_train)
    loss = loss_fn(y_hat, y_train)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    # print(f"{loss:0.3f}")

# Подсчёт эффективности модели
score = (model(X_val).argmax(1) == y_val).sum() / len(y_val) * 100
print(f"Точность модели: {score}%.")
