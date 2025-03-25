from django.db import models

MAX_NAME_LENGTH = 150
MAX_TEXT_LENGTH = 255


class Mailing(models.Model):
    time_of_first_send = models.DateTimeField(
        "Дата и время первой отправки"
    )
    time_of_last_send = models.DateTimeField(
        "Дата и время последней отправки"
    )
    status = models.CharField("Статус", max_length=MAX_NAME_LENGTH)
    message = models.ForeignKey("Message", on_delete=models.CASCADE)
    recipients = models.ManyToManyField("MessageRecipient")
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='owner_mailings')

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return self.name


class Message(models.Model):
    message_title = models.CharField("Заголовок", max_length=MAX_NAME_LENGTH)
    message_text = models.CharField("Текст сообщения", max_length=MAX_TEXT_LENGTH)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.name


class MessageRecipient(models.Model):
    email = models.EmailField("Почта", max_length=MAX_NAME_LENGTH, unique=True)
    name = models.CharField("ФИО", max_length=MAX_NAME_LENGTH)
    middle_name = models.CharField("ФИО", max_length=MAX_NAME_LENGTH)
    surname = models.CharField("ФИО", max_length=MAX_NAME_LENGTH)
    comment = models.TextField("Комментарий")

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

    def __str__(self):
        return self.name


class MailAttempt(models.Model):
    time_of_attempt = models.DateTimeField("Дата и время попытки", auto_now_add=True)
    status = models.CharField("Статус", max_length=MAX_NAME_LENGTH)
    answer = models.CharField("Ответ", max_length=MAX_TEXT_LENGTH)
    mailing = models.ForeignKey("Mailing", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"

    def __str__(self):
        return self.name