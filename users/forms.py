import email
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
)
from django.core.exceptions import ValidationError
from users.models import User

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Имя пользователя"
                   }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control",
                   "placeholder": "Пароль"
                   }
        )
    )

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Имя пользователя"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Адрес электронной почты"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        ),
        help_text="",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Подтверждение пароля"}
        )
    )

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Данный адрес электронной почты уже зарегистрирован в системе"
            )
        return email

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Текущий пароль"}
        )
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Новый пароль"}
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Подтверждение нового пароля"}
        )
    )

class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class':'form-input'}))

    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", "email", "phone_number", "photo"]
        labels = {
            'first_name' : 'Имя',
            'last_name' : 'Фамилия',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
