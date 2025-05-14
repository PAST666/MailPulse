from django import forms
from django.forms import widgets

from .models import Mailing


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = [
            "time_of_first_send",
            "time_of_last_send",
            "message",
            "recipients",
        ]
        widgets = {
            "time_of_first_send": widgets.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "time_of_last_send": widgets.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }
