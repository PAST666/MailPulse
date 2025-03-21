from django.db import models

MAX_NAME_LENGTH = 150
MAX_TEXT_LENGTH = 255

class message(models.Model):
    message_title = models.CharField('Заголовок', max_length=MAX_NAME_LENGTH)
    message_text = models.CharField('Текст сообщения', max_length=MAX_TEXT_LENGTH)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
    
    def __str__(self):
        return self.name

class message_recipient(models.Model):
    email = models.EmailField('Почта', max_length=MAX_NAME_LENGTH, unique=True)
    full_name = models.CharField('ФИО', max_length=MAX_NAME_LENGTH)
    comment = models.TextField('Комментарий', max_length=MAX_TEXT_LENGTH)

    class Meta:
        verbose_name = 'Получатель сообщения'
        verbose_name_plural = 'Получатели сообщений'
    
    def __str__(self):
        return self.name    

