from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order


@receiver(post_save, sender=Order)
def do_something_when_user_updated(sender, instance, created, **kwargs):
    if not created:
        subject = 'Test'
        message = 'Test'
        from_email = 'ad@ex.com'
        send_mail(subject, message, from_email, ['admin@example.com'])
