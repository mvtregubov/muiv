"""Конфигурация приложения."""

from django.apps import AppConfig as DjangoAppConfig


class LearningPlatformConfig(DjangoAppConfig):
    """Настройки регистрации приложения в проекте."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
    verbose_name = "Платформа изучения C++"
