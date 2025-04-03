from django.db import models
from django.conf import settings

MAX_NAME_LENGTH = 150
MAX_TEXT_LENGTH = 255
STATUS_CHOICES = (
    ('SUCCESS', 'Успех'),
    ('FAILED', 'Неуспешно'),
)
class MailAttemptStatus(models.TextChoices):
    SUCCESS = ('SUCCESS', 'Успех')
    FAILED = ('FAILED', 'Неуспешно')

class MailingStatus(models.TextChoices):
    CREATED = ('CREATED', 'Создана')
    STARTED = ('STARTED', 'Запущена')
    COMPLETED = ('COMPLETED', 'Завершена')

#TODO методы def переопределять поля, метод send_mailing, менять выбор, отправлять рассылки получателям 
class Mailing(models.Model):
    time_of_first_send = models.DateTimeField(
        'Дата и время первой отправки'
    )
    time_of_last_send = models.DateTimeField(
        'Дата и время последней отправки'
    )
    status = models.CharField('Статус', choices=MailingStatus.choices, max_length=MAX_NAME_LENGTH)
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='Сообщение')
    recipients = models.ManyToManyField('Recipient', related_name='mailings')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mailings')
    #TODO ordering, permissions
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('time_of_first_send',)
        permissions = [
            ('can_view_all_mailings', 'Может просматривать все рассылки'),
            ('can_view_all_clients', 'Может просматривать всех клиентов'),
            ('can_block_clients', 'Может блокировать всех клиентов'),
            ('can_block_mailings', 'Может отключать все рассылки'),
        ]

    def __str__(self):
        return f'{self.message.title} - {self.status}'


class Message(models.Model):
    title = models.CharField('Заголовок', max_length=MAX_NAME_LENGTH)
    text = models.CharField('Текст сообщения', max_length=MAX_TEXT_LENGTH)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    #TODO ordering, permissions
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.name

    #TODO ordering, permissions из ТЗ
class Recipient(models.Model):
    email = models.EmailField('Почта', max_length=MAX_NAME_LENGTH, unique=True)
    name = models.CharField('Имя', max_length=MAX_NAME_LENGTH)
    middle_name = models.CharField('Отчество', max_length=MAX_NAME_LENGTH, blank=True)
    surname = models.CharField('Фамилия', max_length=MAX_NAME_LENGTH)
    comment = models.TextField('Комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipients')
    #TODO добавить свойство-метод @property full_name,который будет возвращать полное имя ФИО

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'

    def __str__(self):
        return self.name


class MailAttempt(models.Model):
    time_of_attempt = models.DateTimeField('Дата и время попытки', auto_now_add=True)
    status = models.CharField('Статус', choices=MailAttemptStatus.choices, max_length=MAX_NAME_LENGTH)
    response = models.CharField('Ответ', max_length=MAX_TEXT_LENGTH)
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

    def __str__(self):
        return self.name