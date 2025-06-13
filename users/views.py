from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import (
    PasswordResetConfirmView as BasePasswordResetConfirmView
)
from django.contrib.auth.views import (
    PasswordResetView as BasePasswordResetView
)
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DetailView, TemplateView,
                                  UpdateView)
from django.views.generic.edit import UpdateView

from mailings.utils import check_manager

from .forms import (CustomLoginForm, CustomUserCreationForm, ProfileUpdateForm,
                    UserUpdateForm)
from .models import ActivationToken, Profile, User

# TODO pep8


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("main")

    def get_success_url(self):
        return reverse_lazy("main")


class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"
    success_url = reverse_lazy("main")

    def get_success_url(self):
        return reverse_lazy("main")


class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:email_verification_sent")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()

        activation_token = ActivationToken.objects.create(user=user)

        verification_url = self.request.build_absolute_uri(
            reverse_lazy(
                "users:email_verified",
                kwargs={"user_token": str(activation_token.token)},
            ),
        )
        html_message = render_to_string(
            "users/email/verification_email.html",
            {
                "user": user,
                "verification_link": verification_url,
            },
        )

        send_mail(
            "Подтверждение регистрации в MailTop",
            "",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
            html_message=html_message,
        )

        return super().form_valid(form)


class EmailVerificationSendView(TemplateView):
    template_name = "users/email_verification_sent.html"


class VerifyEmailView(TemplateView):
    template_name = "users/email_verified.html"

    def get(self, request, *args, **kwargs):
        try:
            user_token = self.kwargs.get("user_token")
            token = ActivationToken.objects.get(token=user_token)
        except ActivationToken.DoesNotExist:
            return self.render_to_response(
                {"error": "Недействительная ссылка"}
            )
        # TODO сделать проверку что срок действия ссылки не истек

        user = token.user
        user.is_active = True
        user.save()
        token.delete()
        login(request, user)

        return super().get(request, *args, **kwargs)


class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = "profile"
    template_name = "users/profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = (
            f"Страница пользователя: {self.object.user.username}"
        )
        return context


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "users/profile_edit.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["user_form"] = UserUpdateForm(
                self.request.POST, instance=self.request.user
            )
        else:
            context["user_form"] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context["user_form"]
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({"user_form": user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "users:profile_detail", kwargs={"slug": self.object.slug}
        )


class PasswordResetView(BasePasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")


class CustomPasswordResetConfirmView(BasePasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class BlockUserView(LoginRequiredMixin, View):
    template_name = "users/block_user.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def __user_is_manager(self, user):
        if not check_manager(user):
            raise PermissionDenied(
                "У вас нет прав для блокировки пользователей"
            )

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        user = get_object_or_404(User, id=user_id)
        self.__user_is_manager(request.user)

        if not user.is_blocked:
            return render(
                request, self.template_name, context={"blocked_user": user}
            )
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        user = get_object_or_404(User, id=user_id)

        self.__user_is_manager(request.user)
        if user == request.user:
            raise PermissionDenied("Нельзя заблокировать себя")

        user.is_blocked = True
        user.save()
        return redirect(self.success_url)


class UnblockUserView(LoginRequiredMixin, View):
    template_name = "users/unblock_user.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def __user_is_manager(self, user):
        if not check_manager(user):
            raise PermissionDenied(
                "У вас нет прав для разблокировки пользователей"
            )

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        user = get_object_or_404(User, id=user_id)
        self.__user_is_manager(request.user)

        if user.is_blocked:
            return render(
                request, self.template_name, context={"unblocked_user": user}
            )
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        user = get_object_or_404(User, id=user_id)

        self.__user_is_manager(request.user)
        if user == request.user:
            raise PermissionDenied("Нельзя разблокировать себя")

        user.is_blocked = False
        user.save()
        return redirect(self.success_url)
