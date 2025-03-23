from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomLoginForm, CustomUserCreationForm

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'users/login.html'
    def get_success_url(self):
        return reverse_lazy('main')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('logout')
    template_name = 'users/logout.html'

class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('main')
