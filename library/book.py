from uuid import uuid4


class Book:
    def __init__(self, title: str, author: str, year: int) -> None:
        """
        Инициализирует новый объект книги.

        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги. Должен быть в диапазоне от 1 до текущего года.
        """
        self.id: str = str(uuid4())
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = 'в наличии'

    def to_dict(self) -> dict[str, str | int]:
        """
        Преобразует объект Book в словарь для сохранения в JSON.

        :return: Словарь, представляющий книгу.
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | int]) -> 'Book':
        """
        Создает объект Book из словаря, загруженного из JSON.

        :param data: Словарь, представляющий книгу.
        :return: Созданный объект Book.
        """
        book: Book = cls(data['title'], data['author'], data['year'])
        book.id = data['id']
        book.status = data['status']
        return book

    def __str__(self):
        """
        Возвращает строковое представление книги.

        :return: Строка, содержащая ID, название, автора, год издания и статус книги.
        """
        return (f"ID: {self.id}, Название: {self.title}, Автор: {self.author}, Год издания: {self.year}, "
                f"Статус: {self.status}")
