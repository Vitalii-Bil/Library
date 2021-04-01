from django.db.models.signals import post_save

from .models import Order

from django.core.mail import send_mail


@receiver(post_save, sender=Order)
def do_something_when_user_updated(sender, instance, created, **kwargs):
    if not created:
        order_obj = instance
        subject = 'Test'
        message = f'Test'
        from_email = 'ad@ex.com'
        send_mail(subject, message, from_email, ['admin@example.com'])
