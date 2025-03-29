import uuid
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .forms import CustomLoginForm, CustomUserCreationForm, ProfileUserForm
from .models import User, ActivationToken


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("main")


class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"
    next_page = reverse_lazy("main")


class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("password_reset_sent")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()

        activation_token = ActivationToken.objects.create(user=user)
        verification_url = self.request.build_absolute_uri(
            reverse_lazy(
                "users:activate_account", kwargs={"token": str(activation_token.token)}
            ),
        )

        send_mail(
            "Подтверждение регистрации в MailPulse",
            f"Для активации перейдите по ссылке: {verification_url}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUserForm
    template_name = "users/profile.html"
    extra_context = {"title": "Профиль"}

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self) -> str:
        return reverse_lazy("users:profile", args=[self.request.user.pk])


class EmailVerificationSendView(TemplateView):
    template_name = "users/password_reset_sent.html"

class ActivateAccountView(TemplateView):
    template_name = "users/account_activated.html"

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            activation_token = ActivationToken.objects.get(token=token)
            user = activation_token.user
            user.is_active = True
            user.save()
            activation_token.delete()
            return super().get(request, *args, **kwargs)
        except ActivationToken.DoesNotExist:
            # Перенаправление на страницу с ошибкой
            return redirect('activation_error')
