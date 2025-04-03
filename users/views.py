from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView, UpdateView
from django.db import transaction

from .forms import (
    CustomLoginForm,
    CustomUserCreationForm,
    ProfileUserForm,
    UserUpdateForm,
    ProfileUpdateForm,
)
from .models import User, ActivationToken, Profile

# TODO pep8


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("main")


class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"
    success_url = reverse_lazy("main")


class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("email_verification_sent")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()

        activation_token = ActivationToken.objects.create(user=user)
        verification_url = self.request.build_absolute_uri(
            reverse_lazy(
                "email_verified", kwargs={"token": str(activation_token.token)}
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
    extra_context = {"title": "Регистрация"}

    def get_success_url(self) -> str:
        return reverse_lazy("users:profile", args=[self.request.user.pk])


class EmailVerificationSendView(TemplateView):
    template_name = "users/email_verification_sent.html"


class VerifyEmailView(TemplateView):
    template_name = "users/email_verified.html"

    def get(self, request, *args, **kwargs):
        try:
            token = ActivationToken.objects.get(
                token=self.kwargs.get("token"),
            )
        except ActivationToken.DoesNotExist:
            return self.render_to_response({"error": "Недействительная ссылка"})

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
        context["title"] = f"Страница пользователя: {self.object.user.username}"
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
        return reverse_lazy("profile_detail", kwargs={"slug": self.object.slug})
