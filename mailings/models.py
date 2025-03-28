from django.db import models
from django.conf import settings

MAX_NAME_LENGTH = 150
MAX_TEXT_LENGTH = 255
STATUS_CHOICES = (
    ('DONE', 'Выполнена'),
    ('NOT_DONE', 'Не выполнена'),
)


class Mailing(models.Model):
    time_of_first_send = models.DateTimeField(
        'Дата и время первой отправки'
    )
    time_of_last_send = models.DateTimeField(
        'Дата и время последней отправки'
    )
    status = models.CharField('Статус', max_length=MAX_NAME_LENGTH)
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    recipients = models.ManyToManyField('MessageRecipient')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mailings')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return self.name


class Message(models.Model):
    message_title = models.CharField('Заголовок', max_length=MAX_NAME_LENGTH)
    message_text = models.CharField('Текст сообщения', max_length=MAX_TEXT_LENGTH)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.name


class MessageRecipient(models.Model):
    email = models.EmailField('Почта', max_length=MAX_NAME_LENGTH, unique=True)
    name = models.CharField('Имя', max_length=MAX_NAME_LENGTH)
    middle_name = models.CharField('Отчество', max_length=MAX_NAME_LENGTH)
    surname = models.CharField('Фамилия', max_length=MAX_NAME_LENGTH)
    comment = models.TextField('Комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipients')

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'

    def __str__(self):
        return self.name


class MailAttempt(models.Model):
    time_of_attempt = models.DateTimeField('Дата и время попытки', auto_now_add=True)
    status = models.CharField('Статус', choices=STATUS_CHOICES, default='NOT_DONE',max_length=MAX_NAME_LENGTH)
    answer = models.CharField('Ответ', max_length=MAX_TEXT_LENGTH)
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

    def __str__(self):
        return self.name