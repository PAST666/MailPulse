from django.db import models


class MailingManager(models.Manager):
    def for_user(self, user) -> models.QuerySet:
        if user.groups.filter(name="Менеджеры").exists():
            return self.all()
        return self.filter(owner=user)


class MessageManager(models.Manager):
    def for_user(self, user) -> models.QuerySet:
        if user.groups.filter(name="Менеджеры").exists():
            return self.all()
        return self.filter(owner=user)
