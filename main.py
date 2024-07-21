import os

from library.book import Book
from library.library import Library


def clear_screen() -> None:
    """
    Очищает экран консоли.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def pause() -> None:
    """
    Пауза для возможности прочитать результат.
    """
    input('Нажмите Enter для продолжения...')


def display_menu() -> None:
    """
    Отображает меню действий.
    """
    clear_screen()
    print('\nДоступные действия:', '1. Добавить книгу', '2. Удалить книгу',
          '3. Поиск книг', '4. Отобразить все книги',
          '5. Изменить статус книги', '6. Сохранить данные в файл',
          '7. Загрузить данные из файла', '8. Выход', sep='\n', end='\n\n')


def add_book(library: Library) -> None:
    """
    Добавляет книгу в библиотеку.

    :param library: Экземпляр класса `Library` (библиотека).
    """
    title: str = input('Введите название книги: ')
    author: str = input('Введите автора книги: ')

    try:
        year: int = int(input('Введите год издания книги: ').strip())
    except ValueError:
        print('Ошибка ввода. Введите корректное число.')
        pause()
        return

    library.add_book(title, author, year)
    pause()


def delete_book(library: Library) -> None:
    """
    Удаляет книгу из библиотеки.

    :param library: Экземпляр класса `Library` (библиотека).
    """
    book_id: str = input('Введите ID книги, которую нужно удалить: ')
    library.delete_book(book_id)
    pause()


def search_books(library: Library, search_field_map: dict[str, str]) -> None:
    """
    Ищет книги по заданным критериям.

    :param library: Экземпляр класса `Library` (библиотека).
    :param search_field_map: Словарь, где ключи — это строки, представляющие критерии поиска,
                             а значения — это строки, соответствующие полям в данных библиотеки.
    """
    search_criteria: dict[str, str | int] = {}
    print("Введите критерии поиска. Для завершения введите 'конец'.")

    while True:
        search_field: str = input('\nВведите критерий поиска (название/автор/год издания): ').strip().lower()

        if search_field == 'конец':
            break

        if search_field in search_field_map:
            search_value: str | int = input(f'Введите {search_field}: ').strip()

            if search_field == 'год издания':
                try:
                    search_value = int(search_value)
                except ValueError:
                    print('Ошибка ввода. Введите корректное число.')
                    continue

            search_criteria[search_field_map[search_field]] = search_value
        else:
            print("\nНекорректный критерий для поиска. "
                  "Пожалуйста, укажите 'название', 'автор' или 'год издания'.")

    if search_criteria:
        results: list[Book] = library.search_books(**search_criteria)

        if results:
            print('\nРезультаты поиска:')
            for book in results:
                print(book)
        else:
            print('Книги не найдены.')
    else:
        print('Не введены критерии для поиска.')
    pause()


def display_books(library: Library) -> None:
    """
    Отображает все книги в библиотеке.

    :param library: Экземпляр класса `Library` (библиотека).
    """
    print('\nСодержимое библиотеки:')
    library.display_books()
    pause()


def update_book_status(library: Library) -> None:
    """
    Изменяет статус книги.

    :param library: Экземпляр класса `Library` (библиотека).
    """
    book_id: str = input('Введите ID книги: ')
    new_status: str = input('Введите новый статус (в наличии/выдана): ').strip().lower()
    library.update_book_status(book_id, new_status)
    pause()


def save_to_file(library: Library) -> None:
    """
    Сохраняет данные библиотеки в файл.

    :param library: Экземпляр класса `Library` (библиотека).
    """
    file_path = input('Введите путь к файлу для сохранения: ').strip()
    library.save_to_file(file_path)
    pause()


def load_from_file(library: Library) -> None:
    """
    Загружает данные библиотеки из файла.

    :param library: Экземпляр класса `Library` (библиотека).
    """
    file_path = input('Введите путь к файлу для загрузки: ').strip()
    library.load_from_file(file_path)
    pause()


def main() -> None:
    """
    Основная функция для запуска системы управления библиотекой.
    """
    library: Library = Library()
    search_field_map: dict[str, str] = {
        'название': 'title',
        'автор': 'author',
        'год издания': 'year'
    }

    while True:
        display_menu()
        choice: str = input('Выберите действие: ')

        try:
            if choice == '1':
                add_book(library)
            elif choice == '2':
                delete_book(library)
            elif choice == '3':
                search_books(library, search_field_map)
            elif choice == '4':
                display_books(library)
            elif choice == '5':
                update_book_status(library)
            elif choice == '6':
                save_to_file(library)
            elif choice == '7':
                load_from_file(library)
            elif choice == '8':
                break
            else:
                print('Некорректный выбор. Пожалуйста, попробуйте снова.')
                pause()
        except Exception as e:
            print(f'Произошла ошибка: {e}')
            pause()


if __name__ == '__main__':
    main()
