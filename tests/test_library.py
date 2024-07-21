import os
from datetime import date
from json import load, dump
from unittest import TestCase

from library.book import Book
from library.library import Library


class TestLibrary(TestCase):
    def setUp(self) -> None:
        """
        Подготовка данных для тестов.
        """
        self.library: Library = Library()
        self.title: str = "Test book"
        self.author: str = "Test author"
        self.year: int = date.today().year
        self.json_file: str = 'test_books_data.json'
        self.test_data: list[dict[str, str | int]] = [{
            "id": "test-id-1",
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": "в наличии"
        }]

    def tearDown(self) -> None:
        """
        Удаление тестового файла после выполнения тестов.
        """
        if os.path.exists(self.json_file):
            os.remove(self.json_file)

    def test_save_data(self) -> None:
        """
        Тестирование сохранения данных в JSON-файл.
        """
        self.library.add_book(self.title, self.author, self.year)
        self.library.save_to_file(self.json_file)

        self.assertTrue(os.path.exists(self.json_file))

        with open(self.json_file, 'r', encoding='utf-8') as file:
            data: list[dict[str, str | int]] = load(file)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['title'], self.title)
            self.assertEqual(data[0]['author'], self.author)
            self.assertEqual(data[0]['year'], self.year)
            self.assertEqual(data[0]['status'], 'в наличии')

    def test_load_data(self) -> None:
        """
        Тестирование загрузки данных из JSON-файла.
        """
        with open(self.json_file, 'w', encoding='utf-8') as file:
            dump(self.test_data, file, ensure_ascii=False, indent=4)

        self.library.load_from_file(self.json_file)

        self.assertEqual(len(self.library.books), 1)
        book: Book = list(self.library.books.values())[0]
        self.assertEqual(book.title, self.title)
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.year, self.year)
        self.assertEqual(book.status, 'в наличии')

    def test_load_data_invalid_file(self) -> None:
        """
        Тестирование загрузки данных из несуществующего или некорректного JSON-файла.
        """
        with self.assertRaises(FileNotFoundError):
            self.library.load_from_file("non_existing_file.json")

        self.assertEqual(len(self.library.books), 0)

    def test_delete_book(self) -> None:
        """
        Тестирование удаления книги.
        """
        self.library.add_book(self.title, self.author, self.year)
        book_id: str = list(self.library.books.keys())[0]
        self.library.delete_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_search_books(self) -> None:
        """
        Тестирование поиска книг.
        """
        self.library.add_book(self.title, self.author, self.year)
        results: list[Book] = self.library.search_books(title=self.title, author=self.author, year=self.year)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, self.title)

    def test_add_book_valid_year(self) -> None:
        """
        Тестирование добавления книги с корректным годом издания.
        """
        self.library.add_book(self.title, self.author, self.year)
        self.assertEqual(len(self.library.books), 1)
        book_id: str = list(self.library.books.keys())[0]
        book: Book = self.library.books[book_id]
        self.assertEqual(book.title, self.title)
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.year, self.year)
        self.assertEqual(book.status, "в наличии")

    def test_add_book_invalid_year(self) -> None:
        """
        Тестирование добавления книги с некорректным годом издания.
        """
        invalid_years: list[int] = [0, 10000]

        for year in invalid_years:
            with self.assertRaises(ValueError):
                self.library.add_book(self.title, self.author, year)

            self.assertEqual(len(self.library.books), 0)

    def test_update_status(self) -> None:
        """
        Тестирование обновления статуса книги.
        """
        self.library.add_book(self.title, self.author, self.year)
        book_id: str = list(self.library.books.keys())[0]
        self.library.update_book_status(book_id, "выдана")
        self.assertEqual(self.library.books[book_id].status, "выдана")

    def test_update_status_invalid(self) -> None:
        """
        Тестирование обновления статуса с некорректным значением.
        """
        self.library.add_book(self.title, self.author, self.year)
        book_id: str = list(self.library.books.keys())[0]
        self.library.update_book_status(book_id, "неизвестный статус")
        self.assertEqual(self.library.books[book_id].status, "в наличии")
