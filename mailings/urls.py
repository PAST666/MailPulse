from django.urls import path, include
from .views import (
    MessageListView,
    MessageUpdateView,
    MessageDeleteView,
    MessageCreateView,
    MailingListView,
    MailingUpdateView,
    MailingCreateView,
    MailingDeleteView,
    RecipientListView,
    RecipientCreateView,
    RecipientUpdateView,
    RecipientDeleteView,
    MailAttemptListView
)

app_name = "mailings"

message_urls = [
    path("", MessageListView.as_view(), name="message_list"),
    path("create/", MessageCreateView.as_view(), name="message_create"),
    path("<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
]

mailing_urls = [
    path("", MailingListView.as_view(), name="mailing_list"),
    path("create/", MailingCreateView.as_view(), name="mailing_create"),
    path("<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
]

recipient_urls = [
    path("recipient/", RecipientListView.as_view(), name="recipient_list"),
    path("recipient/create", RecipientCreateView.as_view(), name="recipient_create"),
    path(
        "recipient/<int:pk>/update",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient/<int:pk>/delete",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
]

urlpatterns = [
    path("message/", include(message_urls)),
    path("mailing/", include(mailing_urls)),
    path("recipient/", include(recipient_urls)),
    path("mail_attempt/", MailAttemptListView.as_view(), name="mail_attempt"),
]
