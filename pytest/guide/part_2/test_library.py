"""pytest pytest/guide/test_library.py"""


import pytest
from library import Library


# Вынесем повторяющийся код в отдельный метод - воспользуемся фикстурами
@pytest.fixture
def library():  # В названии должно быть то, что возвращаем без префикса "get_"
    books = {1: {"title": "1984", "available": True}}
    readers = {101: {"name": "John Snow", "borrowed": []}}
    return Library(books, readers)


# def test_borrow_book():
#     books = {1: {"title": "1984", "available": True}}
#     readers = {101: {"name": "John Snow", "borrowed": []}}
#     library = Library(books, readers)
#     library.borrow_book(1, 101)  # Тест пройдёт
#     # library.borrow_book(1, 102)  # Тест упадёт

#     assert not library.books[1]["available"]
#     assert 1 in library.readers[101]["borrowed"]


# def test_return_book():
#     books = {1: {"title": "1984", "available": False}}
#     readers = {101: {"name": "John Snow", "borrowed": [1]}}
#     library = Library(books, readers)
#     library.return_book(1, 101)

#     assert library.books[1]["available"]
#     assert 1 not in library.readers[101]["borrowed"]

# # Тест падает гарантированно и это нам нужно
# # def test_borrow_non_existent_book():
# #     books = {1: {"title": "1984", "available": True}}
# #     readers = {101: {"name": "John Snow", "borrowed": []}}
# #     library = Library(books, readers)
# #     library.borrow_book(2, 101)

# # Используем контекстный менеджер
# def test_borrow_non_existent_book():
#     books = {1: {"title": "1984", "available": True}}
#     readers = {101: {"name": "John Snow", "borrowed": []}}
#     library = Library(books, readers)
#     # Ожидаем выпадение заданного исключения
#     # with pytest.raises(KeyError):
#     #     library.borrow_book(2, 101)
#     with pytest.raises(KeyError) as e:
#         library.borrow_book(2, 101)

#     assert "2" in str(e)


def test_borrow_book(library):
    library.borrow_book(1, 101)

    assert not library.books[1]["available"]
    assert 1 in library.readers[101]["borrowed"]


def test_return_book(library):
    # Так как инициализация библиотеки вынесена,
    # где книга в ней, то добавляем её к читателю самостоятельно
    library.books[1]["available"] = False
    library.readers[101]["borrowed"] = [1]
    library.return_book(1, 101)

    assert library.books[1]["available"]
    assert 1 not in library.readers[101]["borrowed"]


def test_borrow_non_existent_book(library):
    with pytest.raises(KeyError) as e:
        library.borrow_book(2, 101)

    assert "2" in str(e)


# Ещё тесты, как пример, что тест - незаменимы
def test_borrow_unavailable_book(library):
    library.books[1]["available"] = False
    with pytest.raises(Exception):
        library.borrow_book(1, 101)


def test_borrow_book_unknown_reader(library):
    with pytest.raises(KeyError):
        library.borrow_book(1, 102)

    assert library.books[1]["available"]


def test_return_book_unknown_reader(library):
    library.books[1]["available"] = False
    with pytest.raises(KeyError):
        library.return_book(1, 102)

    assert not library.books[1]["available"]
