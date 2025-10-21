"""Точка входа для демонстрационного веб-приложения.

Файл создаёт и запускает приложение Django через WSGI. В рамках
учебного примера используется функция execute_from_command_line,
что позволяет запускать встроенный сервер разработки командой
"python project/main.py runserver".
"""

import os
import sys


def main() -> None:
    """Запускает встроенную консоль Django.

    Аргументы командной строки прокидываются в Django. Это позволяет
    выполнять миграции, создавать суперпользователя и стартовать
    dev-сервер без использования manage.py.
    """

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
