from datetime import date
from unittest import TestCase

from library.book import Book


class TestBook(TestCase):
    def setUp(self) -> None:
        """
        Подготовка данных для тестов.
        """
        self.title: str = "Test book"
        self.author: str = "Test author"
        self.year: int = date.today().year
        self.book: Book = Book(self.title, self.author, self.year)
        self.valid_data: dict[str, str | int] = {
            "id": "test-id-1",
            "title": "Test Title",
            "author": "Test Author",
            "year": 2024,
            "status": "в наличии"
        }
        self.invalid_data: dict[str, str | int] = {
            "id": "test-id-2",
            "title": "Another Title",
            "author": "Another Author",
            # отсутствует ключ 'year'
            "status": "выдана"
        }

    def test_book_init(self) -> None:
        """
        Тестирование инициализации объекта Book.
        """
        self.assertIsInstance(self.book.id, str)
        self.assertEqual(self.book.title, self.title)
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.year, self.year)
        self.assertEqual(self.book.status, "в наличии")

    def test_book_str_method(self) -> None:
        """
        Тестирование строкового представления книги.
        """
        expected_str: str = (f"ID: {self.book.id}, Название: {self.title}, Автор: {self.author}, "
                             f"Год издания: {self.year}, Статус: {self.book.status}")

        self.assertEqual(str(self.book), expected_str)

    def test_from_dict(self) -> None:
        """
        Тестирование метода from_dict для создания объекта Book из словаря.
        """
        book: Book = Book.from_dict(self.valid_data)

        self.assertEqual(book.id, self.valid_data["id"])
        self.assertEqual(book.title, self.valid_data["title"])
        self.assertEqual(book.author, self.valid_data["author"])
        self.assertEqual(book.year, self.valid_data["year"])
        self.assertEqual(book.status, self.valid_data["status"])

    def test_from_dict_invalid_data(self) -> None:
        """
        Тестирование метода from_dict с некорректными данными.
        """
        with self.assertRaises(KeyError):
            Book.from_dict(self.invalid_data)
