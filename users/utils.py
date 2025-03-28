from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)
def send_verification_email(user, request):
    """Отправляет email с ссылкой для подтверждения регистрации"""
    verification_link = request.build_absolute_uri(
        reverse('users:verify_email', kwargs={'token': user.email_verification_token})
    )
    
    subject = 'Подтверждение регистрации на сайте MailPulse'
    message = f'Для подтверждения регистрации перейдите по ссылке: {verification_link}'
    
    html_message = render_to_string('users/email/verification_email.html', {
        'user': user,
        'verification_link': verification_link,
    })
    
    recipient = user.email
    logger.info(f"Отправка письма на адрес: {recipient}")
    logger.info(f"Ссылка подтверждения: {verification_link}")
    
    try:
        result = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            html_message=html_message,
            fail_silently=True,
        )
        logger.info(f"Результат отправки: {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка при отправке письма: {str(e)}")
        return False