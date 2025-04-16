from django import forms
from .models import Mailing


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["time_of_first_send", "time_of_last_send", "message", "recipients"]
        #TODO widgets сделать time of first/last DateTimeInput