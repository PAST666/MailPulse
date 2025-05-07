from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomRegisterView,
    VerifyEmailView,
    ProfileUpdateView,
    ProfileDetailView,
    EmailVerificationSendView,
    PasswordResetView,
    CustomPasswordResetConfirmView
)

app_name = "users"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", CustomRegisterView.as_view(), name="register"),
    path(
        "verify_email/<uuid:user_token>/", VerifyEmailView.as_view(), name="email_verified"
    ),
    path(
        "email-verification-sent/",
        EmailVerificationSendView.as_view(),
        name="email_verification_sent",
    ),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path(
        "profile_detail/<str:slug>/", ProfileDetailView.as_view(), name="profile_detail"
    ),
    path(
        "password_reset/",
        PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
            CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
