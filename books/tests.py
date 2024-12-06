from django.test import TestCase
from books.models import Book


class BookTests(TestCase):
    """
    Тесты для модели Book.
    """

    def test_create_book(self):
        """
        Проверяет создание книги в базе данных.
        """

        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            year=2024
        )

        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.year, 2024)

    def test_status_choices(self):
        """
        Проверяет правильность работы статусов книги.
        """

        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            year=2024,
            status='issued'
        )

        self.assertEqual(book.status, 'issued')
