"""Скрипт подготовки демонстрационной SQLite-базы и SQL-дампа."""
from __future__ import annotations

import datetime as dt
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR / "project"
DB_PATH = PROJECT_DIR / "db.sqlite3"
DUMP_DIR = PROJECT_DIR / "database"
DUMP_DIR.mkdir(parents=True, exist_ok=True)
DUMP_PATH = DUMP_DIR / "dump.sql"

if DB_PATH.exists():
    DB_PATH.unlink()

now = dt.datetime(2024, 1, 15, 12, 0, 0)

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

cur.executescript(
    """
    CREATE TABLE django_migrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        applied DATETIME NOT NULL
    );

    CREATE TABLE django_content_type (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_label VARCHAR(100) NOT NULL,
        model VARCHAR(100) NOT NULL,
        UNIQUE(app_label, model)
    );

    CREATE TABLE auth_permission (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        content_type_id INTEGER NOT NULL REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED,
        codename VARCHAR(100) NOT NULL,
        UNIQUE(content_type_id, codename)
    );

    CREATE TABLE auth_group (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(150) NOT NULL UNIQUE
    );

    CREATE TABLE auth_group_permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED,
        permission_id INTEGER NOT NULL REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED,
        UNIQUE(group_id, permission_id)
    );

    CREATE TABLE app_user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password VARCHAR(128) NOT NULL,
        last_login DATETIME NULL,
        is_superuser BOOLEAN NOT NULL,
        username VARCHAR(150) NOT NULL UNIQUE,
        first_name VARCHAR(150) NOT NULL,
        last_name VARCHAR(150) NOT NULL,
        email VARCHAR(254) NOT NULL,
        is_staff BOOLEAN NOT NULL,
        is_active BOOLEAN NOT NULL,
        date_joined DATETIME NOT NULL,
        bio TEXT NOT NULL,
        organization VARCHAR(255) NOT NULL
    );

    CREATE TABLE app_user_groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES app_user(id) DEFERRABLE INITIALLY DEFERRED,
        group_id INTEGER NOT NULL REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED,
        UNIQUE(user_id, group_id)
    );

    CREATE TABLE app_user_user_permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES app_user(id) DEFERRABLE INITIALLY DEFERRED,
        permission_id INTEGER NOT NULL REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED,
        UNIQUE(user_id, permission_id)
    );

    CREATE TABLE django_admin_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_time DATETIME NOT NULL,
        object_id TEXT NULL,
        object_repr VARCHAR(200) NOT NULL,
        action_flag INTEGER NOT NULL,
        change_message TEXT NOT NULL,
        content_type_id INTEGER REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED,
        user_id INTEGER NOT NULL REFERENCES app_user(id) DEFERRABLE INITIALLY DEFERRED
    );

    CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON django_admin_log(content_type_id);
    CREATE INDEX django_admin_log_user_id_c564eba6 ON django_admin_log(user_id);

    CREATE TABLE django_session (
        session_key VARCHAR(40) NOT NULL PRIMARY KEY,
        session_data TEXT NOT NULL,
        expire_date DATETIME NOT NULL
    );

    CREATE INDEX django_session_expire_date_a5c62663 ON django_session(expire_date);

    CREATE TABLE app_course (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(200) NOT NULL,
        description TEXT NOT NULL,
        author_id INTEGER NOT NULL REFERENCES app_user(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        published DATE NOT NULL
    );

    CREATE INDEX app_course_author_id_idx ON app_course(author_id);

    CREATE TABLE app_lesson (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL REFERENCES app_course(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        title VARCHAR(200) NOT NULL,
        content TEXT NOT NULL,
        "order" INTEGER NOT NULL
    );

    CREATE INDEX app_lesson_course_id_idx ON app_lesson(course_id);

    CREATE TABLE app_quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL REFERENCES app_course(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        title VARCHAR(200) NOT NULL,
        duration_minutes INTEGER NOT NULL
    );

    CREATE INDEX app_quiz_course_id_idx ON app_quiz(course_id);

    CREATE TABLE app_question (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL REFERENCES app_quiz(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        text TEXT NOT NULL
    );

    CREATE INDEX app_question_quiz_id_idx ON app_question(quiz_id);

    CREATE TABLE app_answer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER NOT NULL REFERENCES app_question(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        text VARCHAR(255) NOT NULL,
        is_correct BOOLEAN NOT NULL
    );

    CREATE INDEX app_answer_question_id_idx ON app_answer(question_id);

    CREATE TABLE app_result (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES app_user(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        quiz_id INTEGER NOT NULL REFERENCES app_quiz(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        score INTEGER NOT NULL,
        created_at DATETIME NOT NULL
    );

    CREATE INDEX app_result_user_id_idx ON app_result(user_id);
    CREATE INDEX app_result_quiz_id_idx ON app_result(quiz_id);
    """
)

content_types = [
    ("admin", "logentry"),
    ("auth", "permission"),
    ("auth", "group"),
    ("contenttypes", "contenttype"),
    ("sessions", "session"),
    ("app", "user"),
    ("app", "course"),
    ("app", "lesson"),
    ("app", "quiz"),
    ("app", "question"),
    ("app", "answer"),
    ("app", "result"),
]

for idx, (app_label, model) in enumerate(content_types, start=1):
    cur.execute(
        "INSERT INTO django_content_type (id, app_label, model) VALUES (?, ?, ?)",
        (idx, app_label, model),
    )

permission_targets = {
    "admin.logentry": "log entry",
    "auth.permission": "permission",
    "auth.group": "group",
    "contenttypes.contenttype": "content type",
    "sessions.session": "session",
    "app.user": "user",
    "app.course": "course",
    "app.lesson": "lesson",
    "app.quiz": "quiz",
    "app.question": "question",
    "app.answer": "answer",
    "app.result": "result",
}

actions = [
    ("add", "Can add {target}"),
    ("change", "Can change {target}"),
    ("delete", "Can delete {target}"),
    ("view", "Can view {target}"),
]

permission_id = 1
for ct_id, (app_label, model) in enumerate(content_types, start=1):
    key = f"{app_label}.{model}"
    target = permission_targets[key]
    for code, template in actions:
        cur.execute(
            "INSERT INTO auth_permission (id, name, content_type_id, codename) VALUES (?, ?, ?, ?)",
            (
                permission_id,
                template.format(target=target),
                ct_id,
                f"{code}_{model}",
            ),
        )
        permission_id += 1

password_hash = "pbkdf2_sha256$600000$muivdemo$gBogx5l6KvxGcJR12LM0kP8H519k+VtiIUiK4GTOxQo="

cur.execute(
    """
    INSERT INTO app_user (
        id, password, last_login, is_superuser, username, first_name, last_name,
        email, is_staff, is_active, date_joined, bio, organization
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        1,
        password_hash,
        None,
        True,
        "admin",
        "Администратор",
        "Портала",
        "admin@example.com",
        True,
        True,
        now.strftime("%Y-%m-%d %H:%M:%S"),
        "Руководитель программы C++.",
        "МУИВ",
    ),
)

courses = [
    (
        1,
        "Основы языка C++",
        "Базовый курс, охватывающий синтаксис, типы данных и управление памятью.",
        1,
        "2023-09-01",
    ),
    (
        2,
        "Современный C++",
        "Продвинутый курс по стандартам C++17/20, шаблонам и метапрограммированию.",
        1,
        "2023-11-10",
    ),
]
cur.executemany(
    "INSERT INTO app_course (id, title, description, author_id, published) VALUES (?, ?, ?, ?, ?)",
    courses,
)

lessons = [
    (1, 1, "Введение", "История языка C++ и области применения.", 1),
    (2, 1, "Переменные и типы", "Обзор встроенных типов, области видимости и инициализации.", 2),
    (3, 1, "Управление памятью", "Стек, куча и умные указатели.", 3),
    (4, 2, "Стандартная библиотека", "Контейнеры, алгоритмы и итераторы.", 1),
    (5, 2, "Параллельность", "Средства многопоточности в стандарте C++.", 2),
]
cur.executemany(
    "INSERT INTO app_lesson (id, course_id, title, content, \"order\") VALUES (?, ?, ?, ?, ?)",
    lessons,
)

quizzes = [
    (1, 1, "Тест по основам", 15),
    (2, 2, "Тест по современному C++", 20),
]
cur.executemany(
    "INSERT INTO app_quiz (id, course_id, title, duration_minutes) VALUES (?, ?, ?, ?)",
    quizzes,
)

questions = [
    (1, 1, "Какой оператор используется для разыменования указателя?"),
    (2, 1, "Какой заголовок необходимо подключить для работы с std::unique_ptr?"),
    (3, 2, "Какой ключевое слово включает поддержку концептов в C++20?"),
    (4, 2, "Какой класс потока используется для конкурентного выполнения задач?"),
]
cur.executemany(
    "INSERT INTO app_question (id, quiz_id, text) VALUES (?, ?, ?)",
    questions,
)

answers = [
    (1, 1, "*", True),
    (2, 1, "&", False),
    (3, 1, "->", False),
    (4, 1, "[]", False),
    (5, 2, "<memory>", True),
    (6, 2, "<vector>", False),
    (7, 2, "<optional>", False),
    (8, 2, "<thread>", False),
    (9, 3, "concept", True),
    (10, 3, "module", False),
    (11, 3, "requires", False),
    (12, 3, "constexpr", False),
    (13, 4, "std::jthread", True),
    (14, 4, "std::future", False),
    (15, 4, "std::packaged_task", False),
    (16, 4, "std::async", False),
]
cur.executemany(
    "INSERT INTO app_answer (id, question_id, text, is_correct) VALUES (?, ?, ?, ?)",
    answers,
)

results = [
    (1, 1, 1, 2, now.strftime("%Y-%m-%d %H:%M:%S")),
    (2, 1, 2, 1, now.strftime("%Y-%m-%d %H:%M:%S")),
]
cur.executemany(
    "INSERT INTO app_result (id, user_id, quiz_id, score, created_at) VALUES (?, ?, ?, ?, ?)",
    results,
)

migrations = [
    ("contenttypes", "0001_initial"),
    ("auth", "0001_initial"),
    ("admin", "0001_initial"),
    ("app", "0001_initial"),
    ("sessions", "0001_initial"),
    ("contenttypes", "0002_remove_content_type_name"),
    ("auth", "0002_alter_permission_name_max_length"),
    ("auth", "0003_alter_user_email_max_length"),
    ("auth", "0004_alter_user_username_opts"),
    ("auth", "0005_alter_user_last_login_null"),
    ("auth", "0006_require_contenttypes_0002"),
    ("auth", "0007_alter_validators_add_error_messages"),
    ("auth", "0008_alter_user_username_max_length"),
    ("auth", "0009_alter_user_last_name_max_length"),
    ("auth", "0010_alter_group_name_max_length"),
    ("auth", "0011_update_proxy_permissions"),
    ("auth", "0012_alter_user_first_name_max_length"),
]

for app_label, name in migrations:
    cur.execute(
        "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)",
        (app_label, name, now.strftime("%Y-%m-%d %H:%M:%S")),
    )

conn.commit()

with DUMP_PATH.open("w", encoding="utf-8") as dump_file:
    dump_file.write("-- SQL-дамп демонстрационной базы данных Django-проекта по C++\n")
    for line in conn.iterdump():
        dump_file.write(f"{line}\n")

conn.close()

print(f"База данных сохранена в {DB_PATH}")
print(f"SQL-дамп сохранён в {DUMP_PATH}")
