from django.db import models

MAX_NAME_LENGTH = 150
MAX_EMAIL_LENGTH = 150
MAX_TEXT_LENGTH = 255
MAX_PAGINATE_BY = 20


class MailAttemptStatus(models.TextChoices):
    SUCCESS = ("SUCCESS", "Успех")
    FAILED = ("FAILED", "Неуспешно")


class MailingStatus(models.TextChoices):
    CREATED = ("CREATED", "Создана")
    STARTED = ("STARTED", "Запущена")
    COMPLETED = ("COMPLETED", "Завершена")
