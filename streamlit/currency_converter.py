"""Конвертер валют."""

# Запуск: streamlit run путь_к_файлу.py --server.runOnSave True и автоматическое обновление страницы с каждым изменением

import streamlit as st
# import requests


# @st.cache_data(ttl="1 day")  # Декоратор для выполнения метода не каждый раз, а при первом запуске и раз в сутки после
# def get_rates():
#     url = "https://open.er-api.com/v6/latest/RUB"
#     inverse_rates = requests.get(url).json()["rates"]  # Конвертируем ответ в словарь и забираем курсы
#     # Каждый курс меняем на обратный, потому что API отдает курс рубля к валюте, а не валюты к рублю
#     return {x: 1 / y for x, y in inverse_rates.items()}

st.title("Конвертер валют")
st.write("Посчитайте ваш капитал в разных валютах за секунды!")

# Вывод элементов в 2 колонках, если в всю ширину, то не col1. - col2., а st.
col1, col2 = st.columns(2)

rates = {"USD": 84, "KZT": 0.14}# get_rates()
currency = col2.selectbox("Валюта", list(rates))

# При добавлении элементов пользовательского ввода чисел, можно выбрать, как целые, так и дробные числа
count_usd = col1.number_input(currency, min_value=0.0, value=1.0)  # step=1.0 - можно задать шаг

capital = rates[currency] * count_usd
# Вывод текста в success - зелёном, warning - оранжевом и error - красном.
st.success(f"Ваш баланс: {capital:,.2f} RUB.")  # тысячи разделяются запятой
