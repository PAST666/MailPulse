from django.contrib import admin
from mailings.models import Recipient, MailAttempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
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
        "response",
    )
    search_fields = ("status", "answer")
