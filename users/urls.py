from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomRegisterView,
    ProfileUser,
    VerifyEmailView,
    ProfileUpdateView,
    ProfileDetailView,
)

app = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileUser.as_view(), name='profile'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "reset_password.html"), name ='reset_password'),
    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name = "users/password_reset_sent.html"),
        name ='password_reset_sent'
    ),

    # TODO: Можно изменить логику маршрута,
    #  это зависит от кода users/models.py (45 строка кода)
    path('reset/<uuid:token>/', VerifyEmailView.as_view(), name ='password_reset_confirm'),
    # path('reset/<uuid:token>/', VerifyEmailView.as_view(), name ='password_reset_confirm'), вверху password resetconfirmview

    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_done.html"),
        name='password_reset_done'
    ),
    path('profle/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile_detail/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
]

