from django.db import models


class BaseManagerMixin(models.Manager):
    def for_user(self, user) -> models.QuerySet:
        if user.groups.filter(name="Менеджеры").exists():
            return self.all()
        return self.filter(owner=user)


class MessageManager(BaseManagerMixin):
    pass


class MailingManager(BaseManagerMixin):
    pass


class RecipientManager(BaseManagerMixin):
    pass
