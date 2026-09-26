"""Графический калькулятор. Ссылка: https://yana-graphing-calculator.streamlit.app/"""


import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
# from numpy import *


st.title("Графический калькулятор")

functions = ["sin", "cos", "log"]

with st.sidebar:
    max_x = st.number_input("Максимальное значение X", value=1)
    min_x = st.number_input("Минимальное значение X", value=1)
    steps = st.slider("Количество точек", 50, 500)
    grid = st.checkbox("Сетка")
    function = st.selectbox("Функция", functions)
    # Можно задавать функцию текстом
    # function = st.text_input("Формула", value="x")  # Для этого нужно убрать все np., как так импорт изменили и изменить запись функции в y

x = np.linspace(min_x, max_x, steps)
y = getattr(np, function)(x)  # Читаем строку с функцией и передаём её в numpy для отрисовки
# y = eval(function)

figure = plt.figure()
plt.plot(x, y)

if grid:  # Сетка, если нужна
    plt.grid()

st.pyplot(figure)
