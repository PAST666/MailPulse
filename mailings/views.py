from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.views.generic import View, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from .models import Mailing, Message, Recipient, MailingStatus, MailAttempt
from .utils import check_manager
from .managers import MailingManager, MessageManager


class MainView(View):
    def get(self, request):
        return render(request, "mailings/main.html")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailings/message_list.html"
    context_object_name = "messages"

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
    success_url = reverse_lazy("message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    template_name = "mailings/message_update.html"
    fields = ["title", "text"]
    success_url = reverse_lazy("message_list")

    def get_queryset(self):
        return Message.objects.for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailings/message_delete.html"
    success_url = reverse_lazy("message_list")

    def get_queryset(self):
        return Message.objects.for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        return Mailing.objects.for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    template_name = "mailings/mailing_create.html"
    fields = ["message", "recipients", "time_of_first_send", "time_of_last_send"]
    success_url = reverse_lazy("mailing_list")

    def form_valid(self, form):
        # Устанавливаем текущего пользователя как владельца рассылки
        form.instance.owner = self.request.user
        # Устанавливаем начальный статус рассылки
        form.instance.status = MailingStatus.CREATED
        return super().form_valid(form)
    
    def get_queryset(self):
        return Mailing.objects.for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    template_name = "mailings/mailing_update.html"
    fields = '__all__'
    success_url = reverse_lazy("mailing_list")

    def get_queryset(self):
        return Mailing.objects.for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailing_delete.html"
    success_url = reverse_lazy("mailing_list")

    def get_queryset(self):
        return Mailing.objects.for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context
    

class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "mailings/recipient_list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        return Recipient.objects.for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    template_name = "mailings/recipient_create.html"
    fields = ["email", "name",  "middle_name", "surname", "comment"]
    success_url = reverse_lazy("recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    template_name = "mailings/recipient_update.html"
    fields = '__all__'
    success_url = reverse_lazy("recipient_list")

    def get_queryset(self):
        return Recipient.objects.for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "mailings/recipient_delete.html"
    success_url = reverse_lazy("recipient_list")

    def get_queryset(self):
        return Recipient.objects.for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context

class MailAttemptListView(LoginRequiredMixin, ListView):
    model = MailAttempt
    template_name = "mailings/mail_attempt_list.html"
    context_object_name = "mail_attempts"
    
    def get_queryset(self):
        user = self.request.user
        
        # Если пользователь менеджер, показываем все попытки рассылок
        if check_manager(user):
            return MailAttempt.objects.all().select_related('mailing', 'mailing__owner').order_by('-time_of_attempt')
        
        # Иначе показываем только попытки рассылок, принадлежащих пользователю
        return MailAttempt.objects.filter(mailing__owner=user).select_related('mailing').order_by('-time_of_attempt')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        
        # Добавляем статистику
        context["successful_attempts"] = self.get_queryset().filter(status="Успешно").count()
        context["failed_attempts"] = self.get_queryset().filter(status="Не успешно").count()
        context["total_attempts"] = self.get_queryset().count()
        
        return context