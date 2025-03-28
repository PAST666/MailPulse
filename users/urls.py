from django.urls import path
from .views import (
    CustomLoginView, 
    CustomLogoutView, 
    CustomRegisterView, 
    ProfileUser,
    EmailVerificationSentView,
    VerifyEmailView
)

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileUser.as_view(), name='profile'),
    path('email-verification-sent/', EmailVerificationSentView.as_view(), name='email_verification_sent'),
    path('verify-email/<uuid:token>/', VerifyEmailView.as_view(), name='verify_email'),
]
