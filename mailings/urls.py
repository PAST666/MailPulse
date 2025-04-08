from django.urls import path
from .views import MessageListView, MessageUpdateView


urlpatterns = [
    path("messages/", MessageListView.as_view(), name="messages"),
    path(
        "message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
]
