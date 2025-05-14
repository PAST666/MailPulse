import random

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.utils import timezone
from faker import Faker

from mailings.models import Mailing, MailingStatus, Message, Recipient
from users.models import User

fake_data = Faker()


class Command(BaseCommand):
    help = "Заполнение БД случайными данными"

    def create_users(self):
        created_users = []

        for _ in range(10):
            username = fake_data.user_name()
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"Пользователь уже существует, пропускаем"
                    )
                )
                continue

            user = User.objects.create_user(
                username=username,
                first_name=fake_data.first_name(),
                last_name=fake_data.last_name(),
                password=fake_data.password(length=8),
                email=fake_data.email(),
            )
            created_users.append(user)
            self.stdout.write(
                self.style.SUCCESS(f"Пользователь {user} успешно создан")
            )
        return created_users

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
                    self.style.SUCCESS(
                        f"Получатель {recipient.email} успешно создан"
                    )
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING(
                        f"Не удалось создать получателя - такой пользователь уже существует"
                    )
                )

    def create_messages(self, user, num_messages=10):
        for _ in range(random.randint(5, num_messages)):
            message = Message.objects.create(
                title=fake_data.sentence(nb_words=6).rstrip("."),
                text=fake_data.text(),
                owner=user,
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
                time_of_first_send=fake_data.date_time_between(
                    start_date="-30d",
                    end_date="-20d",
                    tzinfo=timezone.get_current_timezone(),
                ),
                time_of_last_send=fake_data.date_time_between(
                    start_date="-10d",
                    end_date="-2d",
                    tzinfo=timezone.get_current_timezone(),
                ),
                status=random.choice(list(MailingStatus)),
            )
            mailing.recipients.set(
                random.sample(
                    list(recipients),
                    k=min(random.randint(3, 5), len(recipients)),
                )
            )
            self.stdout.write(
                self.style.SUCCESS(f"Рассылка {mailing} успешно создана")
            )

    def handle(self, *args, **options):
        for user in self.create_users():
            self.create_recipients(user)
            self.create_messages(user)
            self.create_mailings(user)
