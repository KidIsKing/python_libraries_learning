import base64


def coding_in_file(text_path, encoded_text_path):
    with open(text_path, "rb") as file_text:
        bytes_text_from_file = file_text.read()
        encoded_text_from_file = base64.b64encode(bytes_text_from_file).decode("utf-8")
        print(encoded_text_from_file)

    # Записываем закодированный текст в файл data/encoded_text_file.txt
    with open(encoded_text_path, "w") as file_encoded_text:
        file_encoded_text.write(encoded_text_from_file)

    # Читаем закодированный текст и декодируем его для проверки
    with open(encoded_text_path, "r") as file_encoded_text:
        bytes_text_from_file = file_encoded_text.read()
        decoded_text_from_file = base64.b64decode(bytes_text_from_file).decode("utf-8")
        print(decoded_text_from_file)


if __name__ == "__main__":
    coding_in_file(
        "fastapi/practice/auth/en_and_de_coding/data/text_file.txt",
        "fastapi/practice/auth/en_and_de_coding/data/encoded_text_file.txt"
    )
