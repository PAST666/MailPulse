from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.views.generic import View, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Mailing, Message, Recipient, MailingStatus
from .utils import check_manager


manager_group = Group.objects.get(name='Менеджеры')
manager_group_members = manager_group.user_set.all()

class MessageListView(ListView):
    model = Message
    template_name = 'mailings/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.for_user(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['manager_group_members'] = check_manager(self.request.user) #TODO написать функцию для проверки наличия группы Менеджеры у пользователя
        return context
    