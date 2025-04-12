from django.urls import path
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
)


urlpatterns = [
    path("message/", MessageListView.as_view(), name="message_list"),
    path(
        "message/<int:pk>/update", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message/<int:pk>/delete", MessageDeleteView.as_view(), name="message_delete"
    ),
    path(
        "message/create", MessageCreateView.as_view(), name="message_create"
    ),
    path("mailing/", MailingListView.as_view(), name="mailing_list"),
    path(
    "mailing/<int:pk>/update", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
    "mailing/create", MailingCreateView.as_view(), name="mailing_create"
    ),
    path(
    "mailing/<int:pk>/delete", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path("recipient/", RecipientListView.as_view(), name="recipient_list"),
    path(
    "recipient/create", RecipientCreateView.as_view(), name="recipient_create"
    ),
    path(
    "recipient/<int:pk>/update", RecipientUpdateView.as_view(), name="recipient_update"
    ),
    path(
    "recipient/<int:pk>/delete", RecipientDeleteView.as_view(), name="recipient_delete"
    ),
]
