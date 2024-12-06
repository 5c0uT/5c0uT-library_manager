from django.apps import AppConfig


class BooksConfig(AppConfig):
    """
    Конфигурация приложения Books.

    Этот класс настраивает приложение Books и регистрирует сигнал для отслеживания изменений
    в модели Book после запуска приложения.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Автоинкремент для полей моделей по умолчанию
    name = 'books'  # Имя приложения

    def ready(self):
        """
        Этот метод выполняется при старте приложения, чтобы зарегистрировать сигналы.
        """
        import books.signals  # Импортируем сигнал для обработки изменений в модели Book
