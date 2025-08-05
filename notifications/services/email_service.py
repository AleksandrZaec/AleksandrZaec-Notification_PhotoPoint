from django.core.mail import send_mail
from django.conf import settings


def send_email(recipient, message):
    if not recipient.email:
        return False, "No email address"

    try:
        send_mail(
            subject="Notification",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            fail_silently=False,
        )
        return True, None
    except Exception as e:
        return False, str(e)
