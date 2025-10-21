"""Представления для учебной платформы C++."""

from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Lesson, Quiz, Result


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница с приветствием."""

    courses = Course.objects.all()[:3]
    return render(request, "index.html", {"courses": courses})


def course_list(request: HttpRequest) -> HttpResponse:
    """Отображает полный список доступных курсов."""

    return render(request, "course_list.html", {"courses": Course.objects.all()})


def course_detail(request: HttpRequest, course_id: int) -> HttpResponse:
    """Выводит содержание выбранного курса."""

    course = get_object_or_404(Course, pk=course_id)
    return render(request, "lesson.html", {"course": course, "lessons": course.lessons.all()})


def lesson_detail(request: HttpRequest, lesson_id: int) -> HttpResponse:
    """Показывает конкретный урок курса."""

    lesson = get_object_or_404(Lesson, pk=lesson_id)
    next_lesson = Lesson.objects.filter(course=lesson.course, order__gt=lesson.order).order_by("order").first()
    quiz = lesson.course.quizzes.first()
    return render(
        request,
        "lesson.html",
        {
            "lesson": lesson,
            "next_lesson": next_lesson,
            "quiz": quiz,
        },
    )


def quiz_view(request: HttpRequest, quiz_id: int) -> HttpResponse:
    """Страница прохождения теста."""

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, "quiz.html", {"quiz": quiz})


@login_required
def submit_quiz(request: HttpRequest, quiz_id: int) -> HttpResponse:
    """Обрабатывает отправку ответов теста и сохраняет результат."""

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method != "POST":
        messages.info(request, "Для сдачи теста необходимо отправить форму.")
        return redirect("quiz", quiz_id=quiz.pk)

    score = 0
    for question in quiz.questions.all():
        selected_answer = request.POST.get(f"question_{question.pk}")
        if selected_answer is not None and question.answers.filter(pk=selected_answer, is_correct=True).exists():
            score += 1

    Result.objects.create(user=request.user, quiz=quiz, score=score)
    messages.success(request, "Результаты теста сохранены.")
    return redirect("profile")


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """Личный кабинет пользователя с историей результатов."""

    results = Result.objects.filter(user=request.user).select_related("quiz")
    return render(request, "profile.html", {"results": results})


def demo_login(request: HttpRequest) -> HttpResponse:
    """Упрощённая функция входа для презентации проекта."""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        messages.error(request, "Неверные учётные данные")

    return render(request, "login.html")
