"""pytest -v pytest/guide/part_1/test_string_utils.py"""

import random
import string

import pytest
from unittest.mock import patch
from string_utils import palindrome, remove_stop_words


# Параметризация
# def test_palindrome_true():
#     assert palindrome("stats")
#     assert palindrome("deified")
@pytest.mark.parametrize("s", ["stats", "deified"])
def test_palindrome_true(s):
    assert palindrome(s)


@pytest.mark.parametrize("s", ["hello", "world"])
def test_palindrome_false(s):
    assert not palindrome(s)


# Фикстуры
# def test_palindrome():
#     k = random.randint(1, 10)
#     letters = random.choices(string.ascii_lowercase, k=k)
#     s = "".join(letters) + "".join(reversed(letters))

#     assert palindrome(s)


@pytest.fixture()
def random_palindrome():
    """Генерация случайного палиндрома."""
    k = random.randint(1, 10)
    letters = random.choices(string.ascii_lowercase, k=k)
    return "".join(letters) + "".join(reversed(letters))


def test_palindrome_lowercase(random_palindrome):
    print(random_palindrome)
    assert palindrome(random_palindrome)


def test_palindrome_uppercase(random_palindrome):
    print(random_palindrome)
    assert palindrome(random_palindrome.upper())


# Моки (позволяют результат некоторой функции заменить на желаемый)
def test_remove_stop_words():
    with patch("string_utils._get_stop_words", return_value=["a"]):  # Без этого результат был бы: "cat sat mat"
        assert remove_stop_words("a cat sat on a mat") == "cat sat on mat"
