"""Определения моделей данных для платформы изучения C++."""

from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь системы с дополнительными полями профиля."""

    bio = models.TextField("О себе", blank=True)
    organization = models.CharField("Учебное подразделение", max_length=255, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Course(models.Model):
    """Учебный курс по языку C++."""

    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses", verbose_name="Автор")
    published = models.DateField("Дата публикации")

    class Meta:
        ordering = ["title"]
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self) -> str:  # pragma: no cover - метод удобства отображения
        return self.title


class Lesson(models.Model):
    """Отдельный урок курса."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    title = models.CharField("Название урока", max_length=200)
    content = models.TextField("Текст урока")
    order = models.PositiveIntegerField("Порядковый номер", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.course.title}: {self.title}"


class Quiz(models.Model):
    """Тест для проверки знаний после урока."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes", verbose_name="Курс")
    title = models.CharField("Название теста", max_length=200)
    duration_minutes = models.PositiveIntegerField("Длительность", default=15)

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class Question(models.Model):
    """Вопрос теста."""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions", verbose_name="Тест")
    text = models.TextField("Текст вопроса")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self) -> str:  # pragma: no cover
        return self.text[:50]


class Answer(models.Model):
    """Вариант ответа на вопрос."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", verbose_name="Вопрос")
    text = models.CharField("Текст ответа", max_length=255)
    is_correct = models.BooleanField("Правильный ответ", default=False)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self) -> str:  # pragma: no cover
        return self.text


class Result(models.Model):
    """Результат прохождения теста пользователем."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="results", verbose_name="Пользователь")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results", verbose_name="Тест")
    score = models.PositiveIntegerField("Количество правильных ответов")
    created_at = models.DateTimeField("Дата и время прохождения", auto_now_add=True)

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user} - {self.quiz} ({self.score})"
