from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, CustomLogoutView, CustomRegisterView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "users/reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "users/password_reset_sent.html"), name ='password_reset_done'),
    # path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name ='password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name ='password_reset_complete')
]
