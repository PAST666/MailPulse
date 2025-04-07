from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.views.generic import View, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Mailing, Message, Recipient, MailingStatus


manager_group = Group.objects.get(name='Менеджеры')
manager_group_members = manager_group.user_set.all()