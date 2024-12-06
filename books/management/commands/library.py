from django.core.management.base import BaseCommand
from books.models import Book
from books.signals import update_books_after_save, update_books_after_delete
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from books.utils import load_books, save_books


class Command(BaseCommand):
    """
    Класс для управления библиотекой книг через командную строку.
    Включает в себя добавление, удаление, поиск, вывод списка книг и обновление статуса.
    """

    help: str = 'Управление библиотекой книг'

    def add_arguments(self, parser) -> None:
        """
        Добавляет аргументы командной строки для действия.

        :param parser: объект парсера командной строки.
        :return: None
        """

        parser.add_argument('action', type=str, help='Действие: add, delete, search, list, update_status, help')

    def handle(self, *args, **options) -> None:
        """
        Обрабатывает переданное действие и вызывает соответствующую функцию.

        :param args: Позиционные аргументы командной строки.
        :param options: Словарь с аргументами командной строки.
        :return: None
        """

        action: str = options['action'].lower()

        try:
            if action == 'add':
                self.add_book()
            elif action == 'delete':
                self.delete_book()
            elif action == 'search':
                self.search_books()
            elif action == 'list':
                self.list_books()
            elif action == 'update_status':
                self.update_status()
            elif action == 'help':
                self.display_help()
            else:
                self.stdout.write(
                    "Неизвестное действие. Используйте add, delete, search, list, update_status или help.")

        except Exception as e:
            self.stderr.write(f"Ошибка: {e}")

    def add_book(self) -> None:
        """
        Добавляет книгу в библиотеку.

        Запрашивает у пользователя название книги, автора и год издания,
        а затем добавляет книгу в базу данных и обновляет файл JSON через сигнал.

        :return: None
        """

        title: str = input("Введите название книги: ")
        author: str = input("Введите автора книги: ")
        year: str = input("Введите год издания: ")

        # Добавляем книгу в базу данных через Django ORM
        book: Book = Book.objects.create(title=title, author=author, year=year)

        # Вызываем сигнал для обновления файла JSON после добавления книги
        update_books_after_save(Book, book, created=True)

        self.stdout.write(f"Книга добавлена: {book}")

    def delete_book(self) -> None:
        """
        Удаляет книгу из библиотеки по ID.

        Запрашивает у пользователя ID книги, а затем удаляет её из базы данных и
        обновляет файл JSON через сигнал.

        :return: None
        """

        book_id: str = input("Введите ID книги для удаления: ")
        try:
            book: Book = Book.objects.get(id=book_id)
            book.delete()

            # Вызываем сигнал для обновления файла JSON после удаления книги
            update_books_after_delete(Book, book)

            self.stdout.write(f"Книга с ID {book_id} удалена.")

        except Book.DoesNotExist:
            self.stdout.write(f"Книга с ID {book_id} не найдена.")

    def search_books(self) -> None:
        """
        Ищет книги по полям title, author, или year.

        Запрашивает у пользователя, по какому полю и значению искать книги,
        а затем выводит результаты поиска.

        :return: None
        """

        field: str = input("Введите поле для поиска (title, author, year): ").strip().lower()
        query: str = input("Введите значение для поиска: ").strip()

        filters: dict[str, str] = {field: query}
        books = Book.objects.filter(**filters)

        if books:
            for book in books:
                self.stdout.write(str(book))
        else:
            self.stdout.write("Книги не найдены.")

    def list_books(self) -> None:
        """
        Выводит список всех книг в библиотеке.

        :return: None
        """

        books = Book.objects.all()

        if books:
            for book in books:
                self.stdout.write(str(book))
        else:
            self.stdout.write("Библиотека пуста.")

    def update_status(self) -> None:
        """
        Обновляет статус книги (available/issued).

        Запрашивает у пользователя ID книги и новый статус,
        а затем обновляет статус в базе данных и файл JSON через сигнал.

        :return: None
        """

        book_id: str = input("Введите ID книги для обновления статуса: ")
        new_status: str = input("Введите новый статус (available/issued): ").strip().lower()

        try:
            book: Book = Book.objects.get(id=book_id)

            if new_status in dict(Book.STATUS_CHOICES):
                book.status = new_status
                book.save()

                # Вызываем сигнал для обновления файла JSON после обновления статуса
                update_books_after_save(Book, book, created=False)

                self.stdout.write(f"Статус книги обновлен: {book}")
            else:
                self.stdout.write("Неверный статус.")

        except Book.DoesNotExist:
            self.stdout.write(f"Книга с ID {book_id} не найдена.")

    def display_help(self) -> None:
        """
        Выводит справочную информацию по доступным командам.

        :return: None
        """

        help_text: str = """
Доступные команды:
    add        - Добавить книгу в библиотеку
    delete     - Удалить книгу из библиотеки
    search     - Поиск книг по полям title, author, year
    list       - Вывести список всех книг
    update_status - Обновить статус книги (available/issued)
    help       - Показать информацию о доступных командах

Пример использования:
    python manage.py library add
    python manage.py library delete
    python manage.py library search
    python manage.py library list
    python manage.py library update_status
"""

        self.stdout.write(help_text)
