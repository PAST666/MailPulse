from django.views.generic import (
    View,
    ListView,
    UpdateView,
    DeleteView,
    CreateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from mailings.forms import MailingForm
from .models import Mailing, Message, Recipient, MailAttempt, MailingStatus
from .utils import check_manager


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailings/message_list.html"
    context_object_name = "messages"
    paginate_by = 20

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
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    template_name = "mailings/message_update.html"
    fields = ["title", "text"]
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        return Message.objects.for_user(self.request.user)

    def form_valid(self, form):
        if form.instance.owner != self.request.user:
            return self.handle_no_permission()
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailings/message_delete.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        return Message.objects.for_user(self.request.user)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("mailings.can_view_all_mailings"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_create.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        return Mailing.objects.for_user(self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["message"].queryset = Message.objects.for_user(self.request.user)
        form.fields["recipients"].queryset = Recipient.objects.for_user(
            self.request.user
        )
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = MailingStatus.CREATED
        return super().form_valid(form)
    

class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_update.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        return Mailing.objects.for_user(self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["message"].queryset = Message.objects.for_user(self.request.user)
        form.fields["recipients"].queryset = Recipient.objects.for_user(
            self.request.user
        )
        return form

    def form_valid(self, form):
        if form.instance.owner != self.request.user:
            return self.handle_no_permission()
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailing_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        return Mailing.objects.for_user(self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    # TODO создать шаблон
    template_name = "mailings/mailing_detail.html"
    context_object_name = "mailing"

    def get_queryset(self):
        return Mailing.objects.for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        # TODO реализовать пагинацию для получателей
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получаем и устанавливаем объект
        mailing = self.object
        # mailing = self.get_object()
        if mailing.status == MailingStatus.CREATED:
            mailing.send_mailing()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("mailings:mailing_detail", kwargs={"pk": self.object.pk})


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "mailings/recipient_list.html"
    context_object_name = "recipients"
    paginate_by = 20

    def get_queryset(self):
        return Recipient.objects.for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_group_members"] = check_manager(self.request.user)
        return context


class RecipientDetailView(LoginRequiredMixin, DetailView):
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
    fields = ["email", "name", "middle_name", "surname", "comment"]
    success_url = reverse_lazy("mailings:recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    template_name = "mailings/recipient_update.html"
    fields = ["email", "name", "middle_name", "surname", "comment"]
    success_url = reverse_lazy("mailings:recipient_list")

    def get_queryset(self):
        return Recipient.objects.for_user(self.request.user)

    def form_valid(self, form):
        if form.instance.owner != self.request.user:
            return self.handle_no_permission()
        return super().form_valid(form)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "mailings/recipient_delete.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def get_queryset(self):
        return Recipient.objects.for_user(self.request.user)


class MailAttemptListView(LoginRequiredMixin, ListView):
    model = MailAttempt
    template_name = "mailings/mail_attempt_list.html"
    context_object_name = "mail_attempts"

    def get_queryset(self):
        user = self.request.user

        # Если пользователь менеджер, показываем все попытки рассылок
        if check_manager(user):
            return (
                MailAttempt.objects.all()
                .select_related("mailing", "mailing__owner")
                .order_by("-time_of_attempt")
            )

        # Иначе показываем только попытки рассылок, принадлежащих пользователю
        return (
            MailAttempt.objects.filter(mailing__owner=user)
            .select_related("mailing")
            .order_by("-time_of_attempt")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_manager = check_manager(user)
        context["manager_group_members"] = is_manager

        # Статистика для текущего пользователя
        user_attempts = MailAttempt.objects.filter(mailing__owner=user)
        context["user_successful_attempts"] = user_attempts.filter(
            status="Успех"
        ).count()
        context["user_failed_attempts"] = user_attempts.filter(
            status="Неуспешно"
        ).count()
        context["user_total_attempts"] = user_attempts.count()

        # Статистика для всех пользователей (видна только менеджерам)
        if is_manager:
            all_attempts = MailAttempt.objects.all()
            context["all_successful_attempts"] = all_attempts.filter(
                status="Успешно"
            ).count()
            context["all_failed_attempts"] = all_attempts.filter(
                status="Не успешно"
            ).count()
            context["all_total_attempts"] = all_attempts.count()

        return context
