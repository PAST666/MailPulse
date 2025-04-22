from django.core.management.base import BaseCommand
from mailings.models import Mailing, Message, Recipient
from django.contrib.auth.models import User
from django.utils import timezone
from random import randint, choice
from datetime import timedelta

class Command(BaseCommand):
    help = 'Заполнение БД случайными данными'
    def create_users(self):
        pass
    def create_recipients(self):
        pass
    def create_messages(self):
        pass
    def create_mailings(self):
        pass


    def handle(self, *args, **options):
        pass
