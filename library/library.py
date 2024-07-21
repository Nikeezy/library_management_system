import os.path
from datetime import date
from json import dump, load, JSONDecodeError

from library.book import Book


class Library:
    def __init__(self) -> None:
        """
        Инициализирует новый объект библиотеки.

        Создает пустой словарь для хранения книг.
        """
        self.books: dict[str, Book] = {}

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавляет книгу в библиотеку.

        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги. Должен быть в диапазоне от 1 до текущего года.
        """
        if year < 1 or year > date.today().year:
            raise ValueError('Год издания должен быть в диапазоне от 1 до текущего года.')

        book: Book = Book(title, author, year)
        self.books[book.id] = book
        print('Книга успешно добавлена!')

    def delete_book(self, book_id: str) -> None:
        """
        Удаляет книгу из библиотеки по ее ID.

        :param book_id: ID книги, которую нужно удалить.
        """
        if book_id in self.books:
            del self.books[book_id]
            print('Книга успешно удалена!')
        else:
            print('Книга с таким ID отсутствует.')

    def search_books(self, **kwargs: str | int) -> list[Book]:
        """
        Ищет книги по заданным критериям.

        :param kwargs: Критерии поиска. Ключи должны соответствовать атрибутам книги (title, author, year).
        :return: Список книг, соответствующих критериям поиска.
        """
        results: list[Book] = []

        for book in self.books.values():
            for key, value in kwargs.items():
                book_value: str | int = getattr(book, key)

                if isinstance(value, str):
                    if value.lower() in book_value.lower():
                        results.append(book)
                        break
                elif isinstance(value, int):
                    if book_value == value:
                        results.append(book)
                        break

        return results

    def display_books(self) -> None:
        """
        Отображает все книги в библиотеке.
        """
        if not self.books:
            print('Библиотека пуста.')
        else:
            for book in self.books.values():
                print(book)

    def update_book_status(self, book_id: str, new_status: str) -> None:
        """
        Обновляет статус книги по ее ID.

        :param book_id: ID книги, статус которой нужно обновить.
        :param new_status: Новый статус книги. Должен быть "в наличии" или "выдана".
        """
        if new_status not in {"в наличии", "выдана"}:
            print('Некорректный статус. Статус должен быть "в наличии" или "выдана".')
            return

        if book_id in self.books:
            self.books[book_id].status = new_status
            print('Статус книги изменён!')
        else:
            print('Книга с таким ID отсутствует.')

    def save_to_file(self, file_path: str) -> None:
        """
        Сохраняет книги в JSON-файл.

        :param file_path: Путь к файлу для сохранения.
        """
        if not self.books:
            print('Нет книг для сохранения.')
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                dump(self._books_to_dict(), file, ensure_ascii=False, indent=4)
                print('Данные успешно сохранены!')
        except IOError:
            print('Ошибка записи в файл.')

    def load_from_file(self, file_path: str) -> None:
        """
        Загружает книги из JSON-файла.

        :param file_path: Путь к файлу для загрузки.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError('Файл не найден.')

        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                books_dict: list[dict[str, str | int]] = load(file)
            except JSONDecodeError:
                print('Ошибка декодирования JSON.')
                return

        self.books = {book_data['id']: Book.from_dict(book_data) for book_data in books_dict}

        print('Данные успешно загружены!')

    def _books_to_dict(self) -> list[dict[str, str | int]]:
        """
        Преобразует книги в формат словаря для сохранения в JSON.

        :return: Список словарей, представляющих книги.
        """
        return [book.to_dict() for book in self.books.values()]
