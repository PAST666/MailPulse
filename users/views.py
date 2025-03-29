import uuid

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .forms import CustomLoginForm, CustomUserCreationForm, ProfileUserForm
from users.models import User, ActivationToken


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('main')


class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'
    success_url = reverse_lazy('main')

class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('password_reset_sent')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()

        token = ActivationToken.objects.create(user=user)
        verification_url = self.request.build_absolute_uri(
            reverse_lazy(
                'password_reset_confirm',
                kwargs={"token": str(token.token)}
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
    template_name = 'users/profile.html'
    extra_context = {'title':'Регистрация'}

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', args=[self.request.user.pk])

class EmailVerificationSendView(TemplateView):
    template_name = 'users/password_reset_sent.html'


class VerifyEmailView(TemplateView):
    template_name = 'users/email_verified.html'

    def get(self, request, *args, **kwargs):
        try:
            token = ActivationToken.objects.get(token=self.kwargs.get('token'),)
        except ActivationToken.DoesNotExist:
            return self.render_to_response(
                {"error": "Недействительная ссылка"}
            )

        # TODO: Нужно реализовать логику проверки: Не истек ли срок действия токена

        user = token.user
        user.is_active = True
        user.save()

        token.delete()  # После активации пользователя удаляется токен
        login(request, user)  # авторизуется пользователь

        return super().get(request, *args, **kwargs)

    # TODO переопределить метод form_valid
# TemplateView
# TODO реализовать класс VerifyEmailView - подтверждение
# TODO реализовать класс ProfileView для просмотра и редактирования профиля

# https://dev.to/yahaya_hk/password-reset-views-in-django-2gf2








