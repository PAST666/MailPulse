from django.contrib import admin
from mailings.models import MessageRecipient, MailAttempt


@admin.register(MessageRecipient)
class MessageRecipientAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "name",
        "middle_name",
        "surname",
        "comment",
    )
    search_fields = ("name", "surname", "email")

@admin.register(MailAttempt)
class MailAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "time_of_attempt",
        "status",
        "answer",
    )
    search_fields = ("status", "answer")
