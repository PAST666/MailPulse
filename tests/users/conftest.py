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
    )
    user.groups.create(name="Менеджеры")
    return user

@pytest.fixture
def simple_user():
    user = User.objects.create_user(
        username="simple_user", 
        email="simple_user@test.com",
        first_name="simple_user", 
        last_name="simple_user",
        is_active=True
    ) 
    return user    
