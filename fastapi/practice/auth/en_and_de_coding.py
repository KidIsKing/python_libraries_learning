"""Сайт для проверки кодировки: https://www.base64encode.org/."""


import base64


text = "Hello, world!"

# Кодирование
# encoded = base64.b64encode(text.encode()).decode()

bytes_text = text.encode("utf-8")
encoded_bytes = base64.b64encode(bytes_text)
encoded_text = encoded_bytes.decode("utf-8")
print(encoded_text)

# Декодирование
bytes_text = encoded_text.encode("utf-8")
decoded_bytes = base64.b64decode(bytes_text)
decoded_text = decoded_bytes.decode("utf-8")
print(decoded_text)


with open("fastapi/practice/auth/text.txt", "rb") as file_text:
    encoded_file = base64.b64encode(file_text.read()).decode("utf-8")
with open("fastapi/practice/auth/encoded_text.txt", "w") as file_encoded_text:
    file_encoded_text.write(encoded_text)
with open("fastapi/practice/auth/encoded_text.txt", "r") as file_encoded_text:
    decoded_file_text = base64.b64decode(file_encoded_text.read()).decode("utf-8")
print(encoded_file, decoded_file_text)


text = "Hi"  # 1. Это строка (текст для человека)

# 2. Переводим строку в байты (компьютерный язык) через .encode()
# Было: "Hi" -> Стало: b'Hi' (в памяти это числа 72 и 105)
text_bytes = text.encode("utf-8")

# 3. Кодируем БАЙТЫ в Base64
# Функция b64encode принимает байты и ВОЗВРАЩАЕТ тоже байты!
# Стало: b'SGk='
base64_bytes = base64.b64encode(text_bytes)

# 4. Переводим результат обратно в красивую строку через .decode()
# Чтобы мы могли напечатать это без префикса b'...'
# Было: b'SGk=' -> Стало: "SGk="
final_text = base64_bytes.decode("utf-8")

print(final_text)  # Выведет: SGk=
