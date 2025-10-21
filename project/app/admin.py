"""Регистрация моделей в административной панели."""

from django.contrib import admin

from .models import Answer, Course, Lesson, Question, Quiz, Result, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "organization")
    search_fields = ("username", "email")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published")
    list_filter = ("published",)
    search_fields = ("title", "description")


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "duration_minutes")
    inlines = [QuestionInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    ordering = ("course", "order")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "created_at")
    list_filter = ("quiz", "created_at")
