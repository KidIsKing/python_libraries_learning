import base64
import pytest
from coding_in_file import coding_in_file


def test_coding_in_file(capsys):
    """Тест функции кодирования и декодирования файла."""

    # 1. Arrange (Подготовка)
    # Создаем пути к временным файлам внутри тестовой директории
    original_file = "fastapi/practice/auth/en_and_de_coding/data/text_file.txt"
    encoded_file = "fastapi/practice/auth/en_and_de_coding/data/encoded_text_file.txt"

    # Исходный текст для тестирования
    original_text = "Hello, World! Привет, мир! 123"

    # Записываем исходный текст во временный файл
    original_file.write_text(original_text, encoding="utf-8")

    # Ожидаемая закодированная строка (для проверки)
    expected_encoded = base64.b64encode(original_text.encode("utf-8")).decode("utf-8")

    # 2. Act (Действие)
    # Вызываем тестируемую функцию, передавая строковые пути
    coding_in_file(str(original_file), str(encoded_file))

    # 3. Assert (Проверка)
    # Проверяем, что файл с закодированным текстом был создан
    assert encoded_file.exists(), "Закодированный файл не был создан"

    # Проверяем, что содержимое закодированного файла совпадает с ожидаемым
    actual_encoded = encoded_file.read_text(encoding="utf-8")
    assert actual_encoded == expected_encoded, (
        "Содержимое закодированного файла некорректно"
    )

    # Проверяем вывод в консоль (print), используя фикстуру capsys
    captured = capsys.readouterr()
    assert expected_encoded in captured.out, "Закодированный текст не выведен в консоль"
    assert original_text in captured.out, "Декодированный текст не выведен в консоль"
