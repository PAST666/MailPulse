from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailings.models import Mailing

class Command(BaseCommand):
    help = 'Creates the managers group'

    def __create_managers_group(self):
        group, created = Group.objects.get_or_create(name='Менеджеры')

        permission_names=[
            'can_view_all_messages',
            'can_view_all_mailings',
            "can_view_all_clients",
            'can_block_clients',
            'can_block_mailings',
        ]
        # Получаем content_type для модели Mailing
        content_type = ContentType.objects.get_for_model(Mailing)        
        
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=permission_names
        )
        if not permissions.exists():
            self.stdout.write(self.style.ERROR('Permissions not found'))
            return
        
        group.permissions.set(permissions)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Group "{group.name}" created'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Group "{group.name}" already exists'))

    def handle(self, *args, **options):
        self.__create_managers_group()
