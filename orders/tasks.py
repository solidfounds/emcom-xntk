from celery import task
from django.core.mail import send_mail
from .models import Orden


@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is seccessfully created.
    :param order_id:
    :return:
    """
    order = Orden.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n \n You have successfully placed an order' \
              ' You order is {}.'.format(order.first_name, order.id)
    mail_sent = send_mail(subject, message, 'mar_tp@hotmail.es', [order.email])
    return mail_sent