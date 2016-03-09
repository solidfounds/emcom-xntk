from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from orders.models import Orden

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from io import BytesIO


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        #el pago fue correctamente procesado
        order = get_object_or_404(Orden, id=ipn_obj.invoice)
        #marca la orden como pagada
        order.paid = True
        order.save()
        subject = "My shop - Invoice no. {}".format(order.id)
        message = 'Please, find attached the invoice for you recent purchase.'
        email = EmailMessage(subject, message, 'soldiddfouns@gmail.com', [order.email])
        email.send()
    valid_ipn_received.connect(payment_notification)

