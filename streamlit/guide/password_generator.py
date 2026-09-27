"""Генератор паролей. Ссылка: https://yana-password-generator.streamlit.app/"""


import streamlit as st
from string import ascii_letters, digits, punctuation
import random


st.title("Генератор паролей")

lenght = st.slider("Длина", 8, 24, 16)  # Полоса для выбора длины пароля с указанием мин., макс. и длины по умолчанию
special_symbols = st.checkbox("Использовать спец. символы")  # Галочка на использование или нет пунктуации

if st.button("Сгенерировать"):
    symbols = ascii_letters + digits
    if special_symbols:
        symbols += punctuation

    password = "".join(random.choices(symbols, k=lenght))  # Генерация пароля и приведение его к типу строки из массива
    st.code(password, language="text")  # Отображение блока кода для удобного копирования
