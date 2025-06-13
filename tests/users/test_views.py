import pytest
from users.models import User, ActivationToken
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse

from http import HTTPStatus

@pytest.fixture
def make_referer_client(client):
    def set_referer_client(url):
        client.get(url, HTTP_REFERER=url)
    return set_referer_client

@pytest.mark.django_db
def test_register_user_post_valid(client, mocker):
    mocker.patch("django.core.mail.send_mail")
    data = {
        "username": "Alex",
        "email": "test@test.com",
        "password1": "poiU987^",
        "password2": "poiU987^",
    }
    response = client.post(reverse("users:register"), data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse("users:email_verification_sent")

    user = User.objects.get(email=data["email"])
    assert not user.is_active
    assert ActivationToken.objects.filter(user=user).exists()

@pytest.mark.django_db
def test_register_user_post_invalid(client):
    data = {
        "username": "Alex2",
        "email": "test@test2.com",
        "password1": "432!rewQ",
        "password2": "poiU987*",
    }
    response = client.post(reverse("users:register"), data)
    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=data["email"]).exists()

@pytest.mark.django_db
def test_verify_email_valid(client):
    user = User.objects.create_user(
    username="Alex678",
    email="htmlmail@mail.ru",
    password="4321REw!"        
    )
    user_token = ActivationToken.objects.create(user=user)

    response = client.get(
        reverse(
            "users:email_verified",
            kwargs={"user_token": str(user_token.token)},
        ),        
    )
    assert response.status_code == HTTPStatus.OK
    assert "users/email_verified.html" in [temp.name for temp in response.templates]

@pytest.mark.django_db
def test_verify_email_invalid(client):
    user = User.objects.create_user(
    username="Alex678888",
    email="htmlmail2@mail.ru",
    password="4321REw&"        
    )
    user_token = ActivationToken.objects.create(user=user)

    response = client.get(
        reverse(
            "users:email_verified_",
            kwargs={"user_token": str(user_token.token)},
        ),        
    )
# TODO написать тест некорректной верификации

@pytest.mark.django_db
def test_verify_email_expired_link(client):
    user = User.objects.create_user(
        username="Peter",
        email="test@test.com",
        first_name="test",
        last_name="test",
    )
    user_token = ActivationToken.objects.create(user=user)
    user_token.expires_at = timezone.now() - timedelta(minutes=1)
    user_token.save()
    

    response = client.get(
        reverse(
            "users:email_verified",
            kwargs={"user_token": str(user_token.token)},
        ),        
    )

    assert response.status_code == HTTPStatus.OK
    # TODO после добавления проверки дописать код
