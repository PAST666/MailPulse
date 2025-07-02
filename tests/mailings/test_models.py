import pytest
from mailings.models import Message, Mailing, Recipient, MailAttempt
from datetime import timedelta
from django.utils import timezone


@pytest.mark.django_db
class TestMessageModel:

    @pytest.fixture(autouse=True)
    def setup(self, simple_user5):
        self.message = Message.objects.create(
            title="Заголовок",
            text="Текст",
            owner=simple_user5
        )
        
    def test_str(self):
        assert str(self.message) == "Заголовок"

    def test_owner_fields(self):     
    # написать тест проверки полей модели username/email/id
        assert self.message.owner.username == "simple_user5"
        assert self.message.owner.email == "simple_user5@test.com"
        assert self.message.owner.pk == 1
    # для остальных моделей реализовать проверку str

@pytest.mark.django_db
class TestMailingModel:

    @pytest.fixture(autouse=True)
    def setup(self, simple_user5):
        self.message = Message.objects.create(
            title="Тестовое сообщение",
            text="Текст тестового сообщения",
            owner=simple_user5
        )
        self.mailing = Mailing.objects.create(
            time_of_first_send=timezone.now(),
            time_of_last_send=timezone.now() + timedelta(hours=1),
            status="CREATED",
            message=self.message,
            owner=simple_user5
    )
    
    def test_str(self):
        assert str(self.mailing) == "Тестовое сообщение - CREATED"


@pytest.mark.django_db
class TestRecipientModel:

    @pytest.fixture(autouse=True)
    def setup(self, simple_user5):
        self.recipient = Recipient.objects.create(
            name="Donald",
            surname="Trump",
            email="test@test.com",
            owner=simple_user5
        )
    
    def test_str(self):
        assert str(self.recipient) == "Donald"

@pytest.mark.django_db
class TestMailAttemptModel:

    @pytest.fixture(autouse=True)
    def setup(self, simple_user5):
        self.message = Message.objects.create(
            title="Тестовое сообщение",
            text="Текст тестового сообщения",
            owner=simple_user5
        )
        self.mailing = Mailing.objects.create(
            time_of_first_send=timezone.now(),
            time_of_last_send=timezone.now() + timedelta(hours=1),
            status="CREATED",
            message=self.message,
            owner=simple_user5
        )

        self.mail_attempt = MailAttempt.objects.create(
            status="SUCCESS",
            mailing=self.mailing,
        )

    def test_str(self):
        expected = f"Попытка отправки {self.mail_attempt.mailing.message.title} - {self.mail_attempt.status}"
        assert str(self.mail_attempt) == expected