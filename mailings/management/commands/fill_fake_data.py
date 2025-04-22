from django.core.management.base import BaseCommand
from mailings.models import Mailing, Message, Recipient
from users.models import User
from django.utils import timezone
from random import randint, choice
from datetime import timedelta

class Command(BaseCommand):
    help = 'Заполнение БД случайными данными'
    def create_users(self, num_users=10):
        for num in range(1, num_users + 1):
            username = f'user{num}'
            if User.objects.filter(username = username).exists():
                self.stdout.write(self.style.WARNING(f'Пользователь {username} уже существует, пропускаем'))
                continue

            username = User.objects.create_user(
                username=username,
                first_name=f'Имя{randint(1, 100)}',
                last_name=f'Фамилия{randint(1, 100)}',
                password="password123",
                email=f'{username}@example.com',
                date_joined=timezone.now()
            )
            self.stdout.write(self.style.SUCCESS(f'Пользователь {username} успешно создан'))

    def create_recipients(self, num_recipients=10):
        recipients = [f'recipient{num}' for num in range(1, num_recipients + 1)]
        for recipient in recipients:
            recipient = Recipient.objects.create(
                name = f'Получатель{randint(1, 100)}',
                middle_name = "Отчетство",
                surname = f'Фамилия{randint(1, 100)}',
                email = f'{recipient}@example.com',
                #TODO дописать
                owner=owner
            )
            self.stdout.write(self.style.SUCCESS(f'Получатель {recipient} успешно создан'))

    def create_messages(self, num_messages=10):
        messages = [f'Сообщение{num}' for num in range(1, num_messages + 1)]
        for message in messages:
            message = Message.objects.create(
                title = message,
                text = "Какой-то текст"
            )
            message.title = f'Какой-то текст {randint(1, 100)}'
            message.text = f'Какой-то текст {randint(1, 100)}'
            self.stdout.write(self.style.SUCCESS(f'Сообщение {message} успешно создано'))

    def create_mailings(self, num_mailings=5):
        mailings = [f'Рассылка{num}' for num in range(1, num_mailings + 1)]
        for mailing in mailings:
            message = Message.objects.order_by('?').first()
            user = User.objects.order_by('?').first()
            recipient = Recipient.objects.order_by('?').first()
            mailing = Mailing.objects.create(
                message = message,
                user = user,
                recipient = recipient,
                time_of_first_send = timezone.now(),
                time_of_last_send = timezone.now() + timedelta(hours=1),
                status = 'STARTED'
            )
            self.stdout.write(self.style.SUCCESS(f'Рассылка {mailing} успешно создана'))


    def handle(self, *args, **options):
        self.create_users()
        self.create_recipients()
        self.create_messages()
        self.create_mailings()
