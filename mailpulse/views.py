from django.shortcuts import render
from django.views.generic import TemplateView
from mailings.utils import check_manager
from mailings.models import Mailing, Recipient, MailingStatus

class MainView(TemplateView):
    template_name = "main.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenthicated:
            context["total_mailings"] = Mailing.objects.for_user(self.request.user).count()
            context["active_mailings"] = Mailing.objects.for_user(self.request.user).filter(status=MailingStatus.STARTED).count()
            context["unique_recipients"] = Recipient.objects.for_user(self.request.user).distinct().count()        
        return context