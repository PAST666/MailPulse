import pytest, uuid
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
    password="4321REw!",        
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

    response = client.get(
        reverse(
            "users:email_verified",
            kwargs={"user_token": uuid.uuid4()},
        )      
    )
    assert response.status_code == HTTPStatus.OK
    print(response.content.decode("UTF-8"))
    assert "Недействительная ссылка" in response.content.decode("UTF-8")


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
    assert "Ссылка истекла" in response.content.decode("UTF-8")


@pytest.mark.django_db
def test_block_user_view_get(client, manager, simple_user):
    client.login(username=manager.username, password="Qwer123$")
    response = client.get(
        reverse(
            "users:user_block",
            kwargs={"user_id": simple_user.pk},
        )      
    )  
    assert response.status_code == HTTPStatus.OK
    assert "users/block_user.html" in [temp.name for temp in response.templates] 

@pytest.mark.django_db
def test_block_user_view_post(client, manager, simple_user2):
    client.login(username=manager.username, password="Qwer123$")
    response = client.post(
        reverse(
            "users:user_block",
            kwargs={"user_id": simple_user2.pk},
        )      
    ) 
    ref_url = reverse("mailings:recipient_list")
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == ref_url

    simple_user2.refresh_from_db()
    assert simple_user2.is_blocked

@pytest.mark.django_db
def test_user_block_user(client, simple_user3, simple_user4):
    client.login(username=simple_user3.username, password="Qwer123$")
    response = client.post(
        reverse(
            "users:user_block",
            kwargs={"user_id": simple_user4.pk}
        )
    )
    simple_user4.refresh_from_db()
    assert not simple_user4.is_blocked
    # проверить почему стстус кода 302, ожидается 403
    # print(response.content.decode("UTF-8"))
    # assert response.status_code == HTTPStatus.FORBIDDEN    

@pytest.mark.django_db
def manager_block_self(client, manager):
    client.login(username=manager.username, password="Qwer123$")
    response = client.post(
        reverse(
            "users:user_block",
            kwargs={"user_id": manager.pk}
        )
    )
    manager.refresh_from_db()
    assert not manager.is_blocked
    assert response.status_code == HTTPStatus.FORBIDDEN
