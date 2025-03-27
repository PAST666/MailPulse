from django.db import models
from django.contrib.auth.models import AbstractUser

MAX_NAME_LENGTH = 150

class User(AbstractUser):
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
        return self.name
