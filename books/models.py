from django.db import models


class Book(models.Model):
    """
    Модель книги в библиотеке.

    Атрибуты:
        - title: Название книги
        - author: Автор книги
        - year: Год издания
        - status: Статус книги (доступна или выдана)
    """
    STATUS_CHOICES = [
        ('available', 'В наличии'),
        ('issued', 'Выдана'),
    ]

    title = models.CharField(max_length=255)  # Название книги
    author = models.CharField(max_length=255)  # Автор книги
    year = models.PositiveIntegerField()  # Год издания
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')  # Статус книги

    def __str__(self) -> str:
        """
        Строковое представление книги.

        :return: Строковое описание книги.
        """
        return f"{self.id} - {self.title} by {self.author} ({self.year}) - {self.get_status_display()}"
