class Library:
    def __init__(self, books, readers):
        self.books = books
        self.readers = readers

    def borrow_book(self, book_id, reader_id):
        self.books[book_id]["available"] = False
        self.readers[reader_id]["borrowed"].append(book_id)

    def return_book(self, book_id, reader_id):
        self.books[book_id]["available"] = True
        self.readers[reader_id]["borrowed"].remove(book_id)


# Протестируем код "примерами"
# if __name__ == "__main__":
#     books = {1: {"title": "1984", "available": True}}
#     readers = {101: {"name": "John Snow", "borrowed": []}}
#     library = Library(books, readers)

#     library.borrow_book(1, 101)
#     print(library.books[1]["available"])
#     print(library.readers[101]["borrowed"])

#     library.return_book(1, 101)
#     print(library.books[1]["available"])
#     print(library.readers[101]["borrowed"])
