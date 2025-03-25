from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomLoginForm, CustomUserCreationForm

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('main')


class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'
    next_page = reverse_lazy('logout')

class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('main')

    # TODO переопределить метод form_valid
# TemplateView
# TODO реализовать класс EmailVerificationSendView - страница подтверждения письма
# TODO реализовать класс VerifyEmailView - подтверждение
# TODO реализовать класс ProfileView lдля просмотра и редактирования профиля

# https://dev.to/yahaya_hk/password-reset-views-in-django-2gf2








