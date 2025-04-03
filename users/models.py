import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from datetime import date, timedelta

from .utils import unique_slugify

MAX_NAME_LENGTH = 150
TOKEN_EXPIRES_MINUTES = 15


class User(AbstractUser):
    first_name = models.CharField(
        "Имя", max_length=MAX_NAME_LENGTH, null=True, blank=True
    )
    last_name = models.CharField(
        "Фамилия", max_length=MAX_NAME_LENGTH, null=True, blank=True
    )
    email = models.EmailField("Почта", max_length=MAX_NAME_LENGTH, unique=True)
    photo = models.ImageField(
        "Аватарка",
        upload_to="avatars/",
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        "Телефон",
        max_length=MAX_NAME_LENGTH,
        blank=True,
    )
    country = models.CharField("Страна", max_length=MAX_NAME_LENGTH, blank=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

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
    token = models.UUIDField(
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

    def save(self, *args, **kwargs):
        if not self.expires_at:
            verification_token_expires_minutes = TOKEN_EXPIRES_MINUTES

            self.expires_at = timezone.now() + timezone.timedelta(
                minutes=verification_token_expires_minutes,
            )

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.token}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField("URL", max_length=MAX_NAME_LENGTH, blank=True, unique=True)
    avatar = models.ImageField(
        "Аватар",
        upload_to="images/avatars/%Y/%m/%d/",
        default="images/avatars/default.jpg",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=("png", "jpg", "jpeg"))],
    )
    bio = models.TextField(
        "Информация о себе", max_length=(MAX_NAME_LENGTH * 2), blank=True
    )
    birth_date = models.DateField(
        "Дата рождения",
        null=True,
        blank=True,
    )

    class Meta:
        """
        Сортировка, название таблицы в базе данных
        """

        db_table = "app_profiles"
        ordering = ("user",)
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Возвращение строки
        """
        return self.user.username

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return reverse("profile_detail", kwargs={"slug": self.slug})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
