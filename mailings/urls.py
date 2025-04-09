from django.urls import path
from .views import MessageListView, MessageUpdateView, MessageDeleteView, MessageCreateView


urlpatterns = [
    path("messages/", MessageListView.as_view(), name="messages"),
    path(
        "message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path(
        "message_create/", MessageCreateView.as_view(), name="message_create"
    ),
]
