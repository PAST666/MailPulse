from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from .managers import MailingManager, MessageManager

MAX_NAME_LENGTH = 150
MAX_TEXT_LENGTH = 255

class MailAttemptStatus(models.TextChoices):
    SUCCESS = ("SUCCESS", "Успех")
    FAILED = ("FAILED", "Неуспешно")


class MailingStatus(models.TextChoices):
    CREATED = ("CREATED", "Создана")
    STARTED = ("STARTED", "Запущена")
    COMPLETED = ("COMPLETED", "Завершена")

# TODO ordering, permissions из ТЗ
class Message(models.Model):
    title = models.CharField("Заголовок", max_length=MAX_NAME_LENGTH)
    text = models.CharField("Текст сообщения", max_length=MAX_TEXT_LENGTH)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages"
    )
    permissions = [
    ("can_view_all_messages", "Может просматривать все сообщения"),
    ]
    objects = MessageManager()

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("title",)

    def __str__(self):
        return self.title




# TODO методы def переопределять поля, метод send_mailing, менять выбор, отправлять рассылки получателям
class Mailing(models.Model):
    time_of_first_send = models.DateTimeField("Дата и время первой отправки")
    time_of_last_send = models.DateTimeField("Дата и время последней отправки")
    status = models.CharField(
        "Статус", choices=MailingStatus.choices, max_length=MAX_NAME_LENGTH
    )
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    recipients = models.ManyToManyField("Recipient", related_name="mailings")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mailings"
    )
    objects = MailingManager()

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("time_of_first_send",)
        permissions = [
            ("can_view_all_mailings", "Может просматривать все рассылки"),
            ("can_view_all_clients", "Может просматривать всех клиентов"),
            ("can_block_clients", "Может блокировать всех клиентов"),
            ("can_block_mailings", "Может отключать все рассылки"),
        ]

    def send_mail(self):
        """
        Метод для отправки писем всем получателям рассылки.
        Создает запись о попытке отправки и меняет статус рассылки.
        """
        # Меняем статус рассылки на "Запущена"
        self.status = MailingStatus.STARTED
        self.save()

        success_count = 0
        failed_count = 0

        # Отправляем письма всем получателям
        for recipient in self.recipients.all():
            try:
                # Отправка письма через Django
                send_result = send_mail(
                    subject=self.message.title,
                    message=self.message.text,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )

                # Если письмо успешно отправлено
                if send_result:
                    status = MailAttemptStatus.SUCCESS
                    response = "Письмо успешно отправлено"
                    success_count += 1
                else:
                    status = MailAttemptStatus.FAILED
                    response = "Ошибка при отправке письма"
                    failed_count += 1

            except Exception as e:
                status = MailAttemptStatus.FAILED
                response = f"Ошибка: {str(e)}"
                failed_count += 1

            # Создаем запись о попытке отправки
            MailAttempt.objects.create(status=status, response=response, mailing=self)

        # Обновляем статус рассылки на "Завершена"
        self.status = MailingStatus.COMPLETED
        self.save()

        return {
            "success": success_count,
            "failed": failed_count,
            "total": success_count + failed_count,
        }

    def __str__(self):
        return f"{self.message.title} - {self.status}"


class Recipient(models.Model):
    email = models.EmailField("Почта", max_length=MAX_NAME_LENGTH, unique=True)
    name = models.CharField("Имя", max_length=MAX_NAME_LENGTH)
    middle_name = models.CharField("Отчество", max_length=MAX_NAME_LENGTH, blank=True)
    surname = models.CharField("Фамилия", max_length=MAX_NAME_LENGTH)
    comment = models.TextField("Комментарий")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipients"
    )

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

    @property
    def full_name(self):
        return f"{self.name} {self.middle_name} {self.surname}"

    def __str__(self):
        return self.name


class MailAttempt(models.Model):
    time_of_attempt = models.DateTimeField("Дата и время попытки", auto_now_add=True)
    status = models.CharField(
        "Статус", choices=MailAttemptStatus.choices, max_length=MAX_NAME_LENGTH
    )
    response = models.CharField("Ответ", max_length=MAX_TEXT_LENGTH)
    mailing = models.ForeignKey("Mailing", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"

    def __str__(self):
        return self.name
