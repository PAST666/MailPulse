import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Активация токена для {self.user.email}"