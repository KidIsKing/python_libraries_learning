import requests
import streamlit as st


st.title("Кредитная карта Gold Pro Plus Super от YanaBank с кредитной ставкой до 0.0001%")
st.write("Заполните форму и успейте получить эту суперкарту!")

with st.form("Подать заявку"):
    age = st.number_input("Ваш возраст", min_value=18, max_value=130)
    salary = st.number_input("Ваш доход (в тысячах рублей)", min_value=0.0, step=1.0)
    education = st.checkbox("Наличие высшего образования")
    work = st.checkbox("Наличие постоянного места работы")
    car = st.checkbox("Наличие собственного автомобиля")
    submit = st.form_submit_button("Подать заявку")

if submit:
    data = {
        "age": age,
        "salary": salary,
        "education": education,
        "work": work,
        "car": car
    }

    try:
        response = requests.post("http://127.0.0.1:8000/score", json=data)
        server_answer = response.json()["approved"]
    except (requests.exceptions.RequestException, ValueError, KeyError):
        # Ловим сетевые ошибки, ошибки парсинга JSON и отсутствие ключа
        server_answer = "error"

    if server_answer == "error":
        st.error("Сервис временно недоступен. Попробуйте позже.")
    elif server_answer:
        st.success("Поздравляем! Ваша заявка одобрена!")
    else:
        st.warning("К сожалению, Вам отказано.")
