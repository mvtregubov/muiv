# muiv

Исходный код учебного веб-приложения для изучения языка C++.

## Быстрый старт

```bash
cd project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Развёртывание на PythonAnywhere

1. **Подготовьте учётную запись.** Зарегистрируйтесь или авторизуйтесь на <https://www.pythonanywhere.com/>. На бесплатном тарифе достаточно одного веб-приложения.
2. **Склонируйте репозиторий.** На вкладке **Consoles** откройте новую Bash-консоль и выполните:
   ```bash
   git clone https://github.com/mvtregubov/muiv.git
   cd muiv/project
   ```
   При необходимости можно загрузить архив вручную и распаковать его в домашнем каталоге.
3. **Создайте виртуальное окружение.** PythonAnywhere рекомендует хранить окружения в `~/.virtualenvs`:
   ```bash
   python3.10 -m venv ~/.virtualenvs/muiv
   source ~/.virtualenvs/muiv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **Подготовьте базу данных.** В каталоге `project` уже лежит файл `db.sqlite3` с демо-данными. Если хотите начать с нуля, удалите его и выполните:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. **Настройте веб-приложение.**
   - Перейдите во вкладку **Web** и нажмите **Add a new web app**.
   - Выберите **Manual configuration**, затем нужную версию Python (например, 3.10).
   - В разделе **Code** укажите путь к каталогу `~/muiv/project`.
   - В блоке **Virtualenv** задайте путь `~/.virtualenvs/muiv`.
   - В секции **WSGI configuration file** нажмите «Go to file» и замените путь к модулю на `app.wsgi`:
     ```python
     import os
     import sys

     path = os.path.expanduser('~/muiv/project')
     if path not in sys.path:
         sys.path.append(path)

     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```
6. **Настройте статику.** В разделе **Static files** добавьте правило: URL `/static/` → каталог `~/muiv/project/app/static`.
7. **Перезапустите приложение.** Нажмите кнопку **Reload** в верхней части вкладки **Web**. После этого сайт станет доступен по адресу `https://<ваш_логин>.pythonanywhere.com/`.

Если понадобилось обновить код, выполните `git pull` в Bash-консоли и снова нажмите **Reload**.

## Дополнительные материалы

* `project/db.sqlite3` — готовая SQLite-база данных с демо-данными (учебные курсы, уроки, тесты и результаты). В системе уже создан суперпользователь `admin` с паролем `admin123`. После запуска проекта рекомендуем изменить пароль через Django admin.
* `project/database/dump.sql` — полный SQL-дамп той же базы. Его можно применить вручную, например:

  ```bash
  cd project
  sqlite3 db.sqlite3 < database/dump.sql
  ```

  Дамп включает информацию о миграциях, поэтому после восстановления база готова к работе без дополнительных шагов.
* `scripts/build_sql_dump.py` — генератор, который пересоздаёт `db.sqlite3` и свежий дамп. Скрипт можно запустить, если хотите обновить данные под свои нужды:

  ```bash
  python scripts/build_sql_dump.py
  ```

  При выполнении создаётся новая база и дамп в каталоге `project/database`.

## Причины последних изменений

В ходе предыдущих итераций репозиторий расширили, чтобы выполнить требования к выпускному проекту и облегчить проверку:

1. **Полный каркас Django-приложения.** Добавлены настройки, модели, URL-маршруты, представления и шаблоны, чтобы приложение можно было сразу запустить и демонстрировать функциональность учебной платформы.
2. **Демо-данные и дампы.** Сгенерирована база `db.sqlite3`, миграции и `dump.sql`, позволяющие проверить структуру и данные без ручного наполнения.
3. **Документация по развёртыванию.** README дополнен инструкциями по запуску локально и на PythonAnywhere, чтобы любой проверяющий мог развернуть систему по шагам.

Эти изменения требовались, чтобы предоставить полнофункциональный комплект исходников, соответствующий описанию в техническом задании и запросам на дополнительные материалы.
