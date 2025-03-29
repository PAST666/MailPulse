import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

MAX_NAME_LENGTH = 150


class User(AbstractUser):
    first_name = models.CharField("Имя", max_length=MAX_NAME_LENGTH, null=True, blank=True)
    last_name = models.CharField("Фамилия", max_length=MAX_NAME_LENGTH, null=True, blank=True)
    email = models.EmailField("Почта", max_length=MAX_NAME_LENGTH, unique=True)
    photo = models.ImageField(
        "Аватарка",
        upload_to="avatars/",
        blank=True,
        null=True,
    )
    phone_number = models.IntegerField("Телефон", null=True, blank=True)
    country = models.CharField("Страна", max_length=MAX_NAME_LENGTH, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username


class ActivationToken(models.Model):
    """Модель токен для подтверждения email."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    token = models.UUIDField(  # По желанию, здесь можно использовать
        # другую логику для генерации токена
        "Токен активации",
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    created_at = models.DateTimeField(
        "Создан",
        auto_now_add=True,
    )
    expires_at = models.DateTimeField(
        "Истекает",
    )

    def save(
            self, *args, **kwargs):
        if not self.expires_at:
            verification_token_expires_minutes = 15

            self.expires_at = timezone.now() + timezone.timedelta(
                minutes=verification_token_expires_minutes,
            )

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.token}"
