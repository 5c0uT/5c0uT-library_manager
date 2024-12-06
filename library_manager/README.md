# Library Managеr 

**Library Manager** — это приложение для управления библиотекой книг с использованием Django. Оно позволяет добавлять, удалять, искать и обновлять статус книг через командную строку.

## Установка и настройка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/5c0uT/5c0uT-library_manager.git
    ```
    
3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

## Доступные команды

- **add**: Добавить книгу в библиотеку.
- **delete**: Удалить книгу из библиотеки.
- **search**: Поиск книг по полям title, author, year.
- **list**: Вывести список всех книг.
- **update_status**: Обновить статус книги (available/issued).
- **help**: Показать информацию о доступных командах.

## Пример использования

```bash
python manage.py library add
```
```bash
python manage.py library delete
```
```bash
python manage.py library search
```
```bash
python manage.py library list
```
```bash
python manage.py library update_status
```

```bash
python manage.py library help
```
