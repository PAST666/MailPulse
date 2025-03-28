from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta

from .forms import CustomLoginForm, CustomUserCreationForm, ProfileUserForm
from users.models import User
from .utils import send_verification_email

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
    success_url = reverse_lazy('users:email_verification_sent')
    
    def form_valid(self, form):
        # Сохраняем пользователя, но делаем его неактивным до подтверждения email
        user = form.save(commit=False)
        user.is_active = False  # Пользователь будет активирован после подтверждения email
        user.save()
        
        # Отправляем письмо с подтверждением
        send_verification_email(user, self.request)
        
        return super().form_valid(form)

class EmailVerificationSentView(TemplateView):
    template_name = 'users/email_verification_sent.html'
    extra_context = {'title': 'Подтверждение email'}

class VerifyEmailView(TemplateView):
    template_name = 'users/email_verified.html'
    
    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            user = get_object_or_404(User, email_verification_token=token)
            
            # Проверяем, не истек ли срок действия токена (например, 24 часа)
            token_expiry = user.email_verification_token_created + timedelta(hours=24)
            if now() > token_expiry:
                messages.error(request, 'Срок действия ссылки истек. Пожалуйста, зарегистрируйтесь заново.')
                return redirect('users:register')
            
            # Активируем пользователя
            user.is_active = True
            user.is_email_verified = True
            user.save()
            
            messages.success(request, 'Ваш email успешно подтвержден! Теперь вы можете войти в систему.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, 'Неверная ссылка подтверждения.')
            return redirect('users:register')

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title':'Регистрация'}

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', args=[self.request.user.pk])






# TODO переопределить метод form_valid
# TemplateView
# TODO реализовать класс EmailVerificationSendView - страница подтверждения письма
# TODO реализовать класс VerifyEmailView - подтверждение
# TODO реализовать класс ProfileView для просмотра и редактирования профиля

# https://dev.to/yahaya_hk/password-reset-views-in-django-2gf2








