"""Маршрутизация URL для учебной платформы."""

from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("courses/", views.course_list, name="course_list"),
    path("courses/<int:course_id>/", views.course_detail, name="course_detail"),
    path("lesson/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),
    path("quiz/<int:quiz_id>/", views.quiz_view, name="quiz"),
    path("quiz/<int:quiz_id>/submit/", views.submit_quiz, name="submit_quiz"),
    path("profile/", views.profile, name="profile"),
    path("login/", views.demo_login, name="login"),
]
