import pytest
from mailings.models import Message, Mailing, Recipient, MailAttempt, MailingStatus, MailAttemptStatus
from datetime import timedelta
from django.utils import timezone


@pytest.mark.django_db
class TestMessageModel:

    @pytest.fixture(autouse=True)
    def setup(self, simple_user5,):
        self.message = Message.objects.create(
            title="Заголовок",
            text="Текст",
            owner=simple_user5
        )
        self._owner = simple_user5 
        
    def test_str(self):
        assert str(self.message) == "Заголовок"

    def test_owner_fields(self):     
        assert self.message.owner.username == self._owner.username
        assert self.message.owner.email == self._owner.email
        assert self.message.owner.pk == self._owner.pk
        # assert self.message.owner == self._owner


@pytest.mark.django_db
class TestMailingModel:

    @pytest.fixture(autouse=True)
    def setup(self, simple_user5, mocker):
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
            owner=simple_user5,
        )
        self.recipient = Recipient.objects.create(
            name="Mark",
            surname="Richards",
            email="test123@test.com",
            owner=simple_user5
        )
        self.mailing.recipients.add(self.recipient)
        mocker.patch("django.core.mail.send_mail")
        self._owner = simple_user5
        
    def test_str(self):
        assert str(self.mailing) == "Тестовое сообщение - CREATED"
    
    def test_fields(self):
        assert self.mailing.status == MailingStatus.CREATED
        assert self.mailing.owner == self._owner
        assert self.recipient in self.mailing.recipients.all()
        assert self.mailing.message == self.message
    
    def test_send_mailing_success(self):
        self.mailing.send_mailing()
        self.mailing.refresh_from_db()

        assert self.mailing.status == MailingStatus.COMPLETED

        attempt = MailAttempt.objects.get(mailing=self.mailing)
        assert attempt.status == MailAttemptStatus.SUCCESS

    


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
        self._owner = simple_user5
    
    def test_str(self):
        assert str(self.recipient) == self.recipient.name
    def test_fields(self):
        assert self.recipient.email == "test@test.com"
        assert self.recipient.surname == "Trump"
        assert self.recipient.name == "Donald"

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
        self.mail_attempt.mailing.send_mailing()


    def test_str(self):
        expected = f"Попытка отправки {self.mail_attempt.mailing.message.title} - {self.mail_attempt.status}"
        assert str(self.mail_attempt) == expected
        assert self.mail_attempt.mailing == self.mailing