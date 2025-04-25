import random
from django.core.management.base import BaseCommand
from mailings.models import Mailing, Message, Recipient, MailingStatus
from users.models import User
from django.utils import timezone
from random import randint, choice
from datetime import timedelta
from django.db.utils import IntegrityError
from faker import Faker

fake_data = Faker()


class Command(BaseCommand):
    help = "Заполнение БД случайными данными"

    def create_users(self, num_users=10):
        user_list = []
        for num in range(1, num_users + 1):
            username = f"user{num}"
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"Пользователь {username} уже существует, пропускаем"
                    )
                )
                continue

            username = User.objects.create_user(
                username=username,
                first_name=f"Имя{randint(1, 100)}",
                last_name=f"Фамилия{randint(1, 100)}",
                password="password123",
                email=f"{username}@example.com",
            )
            self.stdout.write(
                self.style.SUCCESS(f"Пользователь {username} успешно создан")
            )
            user_list.append(username)
        return user_list

    def create_recipients(self, user, num_recipients=10):
        for _ in range(random.randint(3, num_recipients)):
            try:
                recipient = Recipient.objects.create(
                    name=fake_data.first_name(),
                    middle_name=fake_data.first_name(),
                    surname=fake_data.last_name(),
                    email=fake_data.email(),
                    owner=user,
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Получатель {recipient.email} успешно создан")
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING(
                        f"Не удалось создать получателя - такой пользователь уже существует"
                    )
                )

    def create_messages(self, user, num_messages=10):
        for _ in range(random.randint (5, num_messages)):
            message = Message.objects.create(
                title=fake_data.sentence(nb_words=6).rstrip("."),
                text=fake_data.text(),
                owner=user
            )
            self.stdout.write(
                self.style.SUCCESS(f"Сообщение {message} успешно создано")
            )

    def create_mailings(self, user, num_mailings=5):
        messages = Message.objects.filter(owner=user)
        recipients = Recipient.objects.filter(owner=user)
        if not messages.exists() or not recipients.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Невозможно создать рассылку, так как нет сообщений или получателей"
                )
            )
            return
        for _ in range(random.randint(3, num_mailings)):
            mailing = Mailing.objects.create(
                message=random.choice(messages),
                owner=user,
                # TODO сделать время с помощью faker
                time_of_first_send=timezone.now(),
                time_of_last_send=timezone.now() + timedelta(hours=1),
                status=MailingStatus.CREATED,
            )
            mailing.recipients.set(
                random.sample(
                    list(recipients), k=min(random.randint(3, 5), len(recipients))
                )
            )
            self.stdout.write(self.style.SUCCESS(f"Рассылка {mailing} успешно создана"))

    def handle(self, *args, **options):
        for user in self.create_users():
            self.create_recipients(user)
            self.create_messages(user)
            self.create_mailings(user)
