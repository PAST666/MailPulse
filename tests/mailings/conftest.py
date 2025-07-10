import pytest
from users.models import User, ActivationToken
from datetime import timedelta
from django.utils import timezone

@pytest.fixture
def manager():
    user = User.objects.create_user(
        username="manager", 
        email="manager@test.com",
        first_name="manager", 
        last_name="manager",
        password="Qwer123$"
    )
    user.groups.create(name="Менеджеры")
    return user

@pytest.fixture
def simple_user5():
    user = User.objects.create_user(
        username="simple_user5",
        email="simple_user5@test.com",
        first_name="simple_user5", 
        last_name="simple_user5",
        is_active=True,
    ) 
    return user

@pytest.fixture
def simple_user2():
    user = User.objects.create_user(
        username="simple_user2",
        email="simple_user2@test.com",
        first_name="simple_user2", 
        last_name="simple_user2",
        is_active=True
    ) 
    return user

@pytest.fixture
def simple_user3():
    user = User.objects.create_user(
        username="simple_user3",
        email="simple_user3@test.com",
        first_name="simple_user3", 
        last_name="simple_user3",
        is_active=True
    ) 
    return user

@pytest.fixture
def simple_user4():
    user = User.objects.create_user(
        username="simple_user4",
        email="simple_user4@test.com",
        first_name="simple_user4", 
        last_name="simple_user4",
        is_active=True
    ) 
    return user
