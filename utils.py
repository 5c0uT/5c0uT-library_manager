from books.models import Book


def load_books_from_db() -> list[Book]:
    """
    Загружает все книги из базы данных.

    :return: Список всех книг, представленных в базе данных.
    """
    return Book.objects.all()


def get_book_by_id(book_id: int) -> Book:
    """
    Получает книгу по ID из базы данных.

    :param book_id: ID книги.
    :return: Экземпляр модели Book.
    :raises Book.DoesNotExist: Если книга с данным ID не найдена.
    """
    try:
        return Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise Book.DoesNotExist(f"Книга с ID {book_id} не найдена.")
