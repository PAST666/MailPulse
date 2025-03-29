from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, CustomLogoutView, CustomRegisterView, ProfileUser, EmailVerificationSendView, ActivateAccountView



app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path('email-verification-sent/', EmailVerificationSendView.as_view(), name='email_verification_sent'),
    path('activate/<uuid:token>/', ActivateAccountView.as_view(), name='activate_account'),
]
