import pytest
from users.models import User, ActivationToken
from datetime import timedelta
from django.utils import timezone


@pytest.mark.django_db
def test_new_user():
    user = User.objects.create_user(
        username="test", 
        email="test@test.com",
        first_name="test", 
        last_name="test",
    )
    assert user.email == "test@test.com"
    assert user.username == "test"
    assert user.first_name == "test"
    assert user.last_name == "test"
    assert user.is_active == True
    assert user.is_blocked == False

    
@pytest.mark.django_db
def test_user_str():
    user = User.objects.create_user(
        username="Peter",
        email="test@test.com",
        first_name="test",
        last_name="test",
    )
    assert str(user) == "Peter"

@pytest.mark.django_db
def test_full_name_field():
    user_first = User.objects.create_user(
    username="test1", 
    email="test1@test.com",
    )
    user_second = User.objects.create_user(
    username="test2", 
    email="test2@test.com",
    first_name="Jack"
    )
    user_third = User.objects.create_user(
    username="test3", 
    email="test3@test.com",
    last_name="Dickson"
    )
    user_fourth = User.objects.create_user(
    username="test4", 
    email="test4@test.com",
    first_name="Jack",
    last_name="Dickson"
    )
    assert user_first.full_name == ""
    assert user_second.full_name == "Jack"
    assert user_third.full_name == "Dickson"
    assert user_fourth.full_name == "Jack Dickson"

@pytest.mark.django_db
def test_activation_token_str():
    user = User.objects.create_user(
        username="Peter",
        email="test@test.com",
        first_name="test",
        last_name="test",
    )
    token = ActivationToken.objects.create(user=user)

    assert str(token) == f"{token.user.username} -> {token.token}"

@pytest.mark.django_db
def test_expires_time_default():
    user = User.objects.create_user(
        username="Peter",
        email="test@test.com",
        first_name="test",
        last_name="test",
    )
    token = ActivationToken.objects.create(user=user)
    time_end = token.created_at + timedelta(minutes=15)


    assert abs((token.expires_at - time_end).total_seconds()) < 1

@pytest.mark.django_db
def test_activation_token_is_valid():
    user = User.objects.create_user(
        username="Peter",
        email="test@test.com",
        first_name="test",
        last_name="test",
    )
    token = ActivationToken.objects.create(user=user)

    assert token.token_is_valid() == True

@pytest.mark.django_db
def test_activation_token_not_is_valid():
    user = User.objects.create_user(
        username="Peter",
        email="test@test.com",
        first_name="test",
        last_name="test",
    )
    token = ActivationToken.objects.create(user=user)

    token.expires_at = timezone.now() - timedelta(minutes=1)
    assert token.token_is_valid() == False    

@pytest.mark.django_db
def test_create_email_correct():
    user = User.objects.create_user(
        username="test", 
        email="test@test.com"
    )

    assert user.email == "test@test.com"

@pytest.mark.django_db
def test_slug():
    user = User.objects.create_user(
        username="a"*157, 
        email="test@test.com"
    )
    assert len(user.profile.slug) == len(user.username)

@pytest.mark.django_db
def bad_word_in_bio():
    user = User.objects.create_user(
        username="test",
        email="test@test.com",
        bio="My name is bXXXb"
    )
    assert "XXX" in user.bio
