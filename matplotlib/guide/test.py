import matplotlib.pyplot as plt


# Количество координат должно быть одинаковым
x = [1, 3, 5, 7, 9]
y = [2, 4, 6, 8, 10]

plt.plot(x, y)  # Простой график - линия по точкам
plt.savefig("matplotlib/guide/test.png")
