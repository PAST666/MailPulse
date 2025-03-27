from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .forms import CustomLoginForm, CustomUserCreationForm, ProfileUserForm
from users.models import User

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
    success_url = reverse_lazy('main')

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title':'Регистрация'}

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile',args=[self.request.user.pk])






    # TODO переопределить метод form_valid
# TemplateView
# TODO реализовать класс EmailVerificationSendView - страница подтверждения письма
# TODO реализовать класс VerifyEmailView - подтверждение
# TODO реализовать класс ProfileView для просмотра и редактирования профиля

# https://dev.to/yahaya_hk/password-reset-views-in-django-2gf2








