from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from books.models import Book
import json
import os

# Путь к файлу, в котором сохраняются данные о книгах
BOOKS_JSON_FILE = os.path.join(os.path.dirname(__file__), 'books.json')


@receiver(post_save, sender=Book)
def update_books_after_save(sender, instance, created, **kwargs):
    """
    Сигнал для обновления файла JSON после добавления или изменения книги.

    :param sender: Модель, которая отправила сигнал (Book).
    :param instance: Экземпляр модели (книга).
    :param created: Булев флаг, который показывает, была ли книга только что создана.
    :param kwargs: Дополнительные аргументы сигнала.
    """
    # Загружаем текущие данные из файла
    books = load_books()

    if created:
        # Добавляем книгу в список, если она была только что создана
        books.append(instance)
    else:
        # Обновляем книгу в списке
        for i, book in enumerate(books):
            if book['id'] == instance.id:
                books[i] = instance

    # Сохраняем обновленные данные в JSON файл
    save_books(books)


@receiver(post_delete, sender=Book)
def update_books_after_delete(sender, instance, **kwargs):
    """
    Сигнал для обновления файла JSON после удаления книги.

    :param sender: Модель, которая отправила сигнал (Book).
    :param instance: Экземпляр модели, который был удален.
    :param kwargs: Дополнительные аргументы сигнала.
    """
    # Загружаем текущие данные из файла
    books = load_books()

    # Удаляем книгу из списка
    books = [book for book in books if book['id'] != instance.id]

    # Сохраняем обновленные данные в JSON файл
    save_books(books)


def load_books():
    """
    Загружает список книг из файла JSON.

    :return: Список книг.
    """
    if os.path.exists(BOOKS_JSON_FILE):
        with open(BOOKS_JSON_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []


def save_books(books):
    """
    Сохраняет список книг в файл JSON.

    :param books: Список книг для сохранения.
    :return: None
    """
    with open(BOOKS_JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(books, file, ensure_ascii=False, indent=4)
