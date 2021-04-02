from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
#  from .tasks import order_in_progress_mail as celery_order_in_progress_mail


@receiver(post_save, sender=Order)
def post_post_save(sender, instance, **kwargs):
    #  celery_order_in_progress_mail.delay(instance.email)
    if kwargs['created']:  # true if the instance is created
        send_mail(
            subject="Your order",
            message="Your order in progress.",
            from_email="ex@ex.com",
            recipient_list=[f'{instance.email}'],
            fail_silently=False
        )
