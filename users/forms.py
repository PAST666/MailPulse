import email
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
)
from django.core.exceptions import ValidationError
from .models import User, Profile


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Имя пользователя"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        )
    )


class CustomUserCreationForm(UserCreationForm):

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
            attrs={
                "class": "form-control",
                "placeholder": "Подтверждение нового пароля",
            }
        )
    )


# class ProfileUserForm(forms.ModelForm):
#     username = forms.CharField(
#         disabled=True,
#         label="Логин",
#         widget=forms.TextInput(attrs={"class": "form-input"}),
#     )
#     email = forms.CharField(
#         disabled=True,
#         label="E-mail",
#         widget=forms.TextInput(attrs={"class": "form-input"}),
#     )

#     class Meta:
#         model = User
#         fields = [
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "phone_number",
#             "photo",
#         ]
#         labels = {
#             "first_name": "Имя",
#             "last_name": "Фамилия",
#             "email": "Имаил",
#         }

#         widgets = {
#             "first_name": forms.TextInput(attrs={"class": "form-input"}),
#             "last_name": forms.TextInput(attrs={"class": "form-input"}),
#             "birth_date": forms.DateInput(
#                 attrs={"class": "form-input", "type": "date"}
#             ),
#         }


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )
            self.fields["username"].widget.attrs["readonly"] = True
            self.fields["email"].widget.attrs["readonly"] = True
            self.fields["username"].label = "Логин"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        if (
            email
            and User.objects.filter(email=email).exclude(username=username).exists()
        ):
            raise forms.ValidationError("Email адрес должен быть уникальным")
        return email


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ("slug", "birth_date", "bio", "avatar")

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы обновления
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )
            self.fields["birth_date"].widget = forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "autocomplete": "off",
                }
            )
            self.fields["slug"].widget.attrs["readonly"] = True
