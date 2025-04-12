from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomRegisterView,
    # ProfileUser,
    VerifyEmailView,
    ProfileUpdateView,
    ProfileDetailView,
    EmailVerificationSendView,
)

app = "users"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", CustomRegisterView.as_view(), name="register"),
    path(
        "verify_email/<uuid:token>/", VerifyEmailView.as_view(), name="email_verified"
    ),
    path(
        "email-verification-sent/",
        EmailVerificationSendView.as_view(),
        name="email_verification_sent",
    ),
    path("profle/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path(
        "profile_detail/<str:slug>/", ProfileDetailView.as_view(), name="profile_detail"
    ),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_complete",
    ),
]
