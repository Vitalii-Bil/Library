from celery import shared_task
from django.core.mail import send_mail


@shared_task
def order_in_progress_mail(email):
    '''Function for celery sending mail, when customer's order in progress'''
    send_mail(
            subject="Your order",
            message="Your order in progress.",
            from_email="ex@ex.com",
            recipient_list=[f'{email}'],
            fail_silently=False
        )


@shared_task
def order_ready_send_mail(email):
    '''Function for celery sending mail, when order was sent to customer'''
    send_mail(
            subject="Your order",
            message="Your order was sent.",
            from_email="ex@ex.com",
            recipient_list=[f'{email}'],
            fail_silently=False
        )
