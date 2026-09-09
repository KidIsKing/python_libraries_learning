import torch


data = torch.load("pytorch/guide/part_2/data/wine-red.pt")
print(data.shape)  # torch.Size([1599, 12]) - 1599 записей, 11 признаков и одна колонка с оценкой сомелье

index = torch.randperm(data.shape[0])
data = data[index]

X, y = data[:, :-1], data[:, -1:]
X_train, X_val = X[:1000], X[1000:]
y_train, y_val = y[:1000], y[1000:]
print(X_train.shape, y_train.shape, X_val.shape, y_val.shape)

# Данные для нормализации подбираем по тренировочным данным
mean = X_train.mean(0)  # Передаем 0 в качестве аргумента, чтобы посчитать значения в каждой колонке
std = X_train.std(0)
# Нормализуем все данные
X_train = (X_train - mean) / std
X_val = (X_val - mean) / std

torch.save(X_train, "X_train.pt")
torch.save(X_val, "X_val.pt")
torch.save(y_train, "y_train.pt")
torch.save(y_val, "y_val.pt")