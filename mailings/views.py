from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.views.generic import View, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from .models import Mailing, Message, Recipient, MailingStatus
from .utils import check_manager
from .managers import MailingManager, MessageManager


class MainView(View):
    def get(self, request):
        return render(request, "mailings/main.html")


manager_group = Group.objects.get(name="Менеджеры")
manager_group_members = manager_group.user_set.all()


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailings/message_list.html"
    context_object_name = "messages"
    login_url = "/users/login/"

    def get_queryset(self):
        return Message.objects.for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    template_name = "mailings/message_update.html"
    fields = ["title", "text"]
    login_url = "/users/login/"
    success_url = reverse_lazy("messages")

    def get_queryset(self):
        return Message.objects.for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context
    
class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailings/message_delete.html"
    success_url = reverse_lazy("messages")
    login_url = "/users/login/"

    def get_queryset(self):
        return Message.objects.for_user(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = "mailings/message_create.html"
    fields = ["title", "text"]
    login_url = "/users/login/"
    success_url = reverse_lazy("messages")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)







