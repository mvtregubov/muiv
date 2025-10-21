"""Начальная миграция для моделей приложения."""
from __future__ import annotations

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    """Создаёт основные таблицы платформы обучения C++."""

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Указывает, что пользователь обладает всеми правами без их явного назначения.",
                        verbose_name="Статус суперпользователя",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={"unique": "Пользователь с таким именем уже существует."},
                        help_text="Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_",
                        max_length=150,
                        unique=True,
                        verbose_name="Имя пользователя",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="Имя")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="Фамилия")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="Адрес электронной почты")),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Указывает, может ли пользователь входить в админ-панель.",
                        verbose_name="Статус персонала",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Отметьте, если пользователь должен считаться активным. Снимите отметку вместо удаления аккаунта.",
                        verbose_name="Активен",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now, verbose_name="Дата регистрации"),
                ),
                ("bio", models.TextField(blank=True, verbose_name="О себе")),
                ("organization", models.CharField(blank=True, max_length=255, verbose_name="Учебное подразделение")),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Группы, к которым принадлежит пользователь.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="Группы",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Конкретные права, назначенные пользователю.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="Права",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                ("published", models.DateField(verbose_name="Дата публикации")),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courses",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Quiz",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Название теста")),
                ("duration_minutes", models.PositiveIntegerField(default=15, verbose_name="Длительность")),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quizzes",
                        to="app.course",
                        verbose_name="Курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тест",
                "verbose_name_plural": "Тесты",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Название урока")),
                ("content", models.TextField(verbose_name="Текст урока")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядковый номер")),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="app.course",
                        verbose_name="Курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "Урок",
                "verbose_name_plural": "Уроки",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField(verbose_name="Текст вопроса")),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="app.quiz",
                        verbose_name="Тест",
                    ),
                ),
            ],
            options={
                "verbose_name": "Вопрос",
                "verbose_name_plural": "Вопросы",
            },
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=255, verbose_name="Текст ответа")),
                ("is_correct", models.BooleanField(default=False, verbose_name="Правильный ответ")),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="app.question",
                        verbose_name="Вопрос",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ответ",
                "verbose_name_plural": "Ответы",
            },
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.PositiveIntegerField(verbose_name="Количество правильных ответов")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Дата и время прохождения"),
                ),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to="app.quiz",
                        verbose_name="Тест",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Результат",
                "verbose_name_plural": "Результаты",
                "ordering": ["-created_at"],
            },
        ),
    ]
