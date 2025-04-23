import time
import random
from django.core.management.base import BaseCommand
from mailings.models import Mailing, Message, Recipient, MailingStatus
from users.models import User
from django.utils import timezone
from random import randint, choice
from datetime import timedelta
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Заполнение БД случайными данными'
    def create_users(self, num_users=10):
        user_list = []
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
            )
            self.stdout.write(self.style.SUCCESS(f'Пользователь {username} успешно создан'))
            user_list.append(username)
        return user_list

    def create_recipients(self, user, num_recipients=10):
        recipients = [f'recipient{num}' for num in range(1, num_recipients + 1)]
        for recipient in recipients:
            timestamp = int(time.time() * 1000)
            random_suffix = random.randint(10000, 99999)
            current_email = f"recipient{timestamp}_{random_suffix}@example.com"
            try:
                recipient = Recipient.objects.create(
                    name = f'Получатель{randint(1, 100)}',
                    middle_name = "Отчетство",
                    surname = f'Фамилия{randint(1, 100)}',
                    email = f'{recipient}@example.com',
                    owner=user
                )
                self.stdout.write(self.style.SUCCESS(f'Получатель {recipient} успешно создан'))
            except IntegrityError:
                # Если все же возникла ошибка уникальности, просто пропускаем этого получателя
                self.stdout.write(self.style.WARNING(f'Не удалось создать получателя с email {current_email} - такой email уже существует'))
                time.sleep(0.01)
                continue

    def create_messages(self, user, num_messages=10):
        messages = [f'Сообщение{num}' for num in range(1, num_messages + 1)]
        for message in messages:
            message = Message.objects.create(
                title = "Сообщение {num}",
                text = "Какой-то текст",
                owner=user
            )
            message.title = f'Какой-то текст {randint(1, 100)}'
            message.text = f'Какой-то текст {randint(1, 100)}'
            self.stdout.write(self.style.SUCCESS(f'Сообщение {message} успешно создано'))

    def create_mailings(self, user, num_mailings=5):
        mailings = [f'Рассылка{num}' for num in range(1, num_mailings + 1)]
        for mailing_name in mailings:
            message = Message.objects.order_by('?').first()
            recipient_email = f'recipient{mailing_name}@example.com'

            recipient = Recipient.objects.get_or_create(
                email=recipient_email,
                defaults={'owner': user}
            )

            if message and user:
                mailing = Mailing.objects.create(
                    message = message,
                    owner = user,
                    time_of_first_send = timezone.now(),
                    time_of_last_send = timezone.now() + timedelta(hours=1),
                    status = MailingStatus.CREATED,
                )
                for recipient in Recipient.objects.filter(owner=user):
                    mailing.recipients.add(recipient)
                self.stdout.write(self.style.SUCCESS(f'Рассылка {mailing_name} успешно создана'))
            else:
                self.stdout.write(self.style.ERROR('Не удалось создать рассылку: отсутствует сообщение, пользователь или получатель'))


    def handle(self, *args, **options):
        for user in self.create_users():
            self.create_recipients(user)
            self.create_messages(user)
            self.create_mailings(user)
