from django.shortcuts import render
from .models import OrderItem
from .forms import OrdenCreateForm
from cart.cart import Cart
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import  reverse
# Create your views here.
from  .tasks import order_created
from django.contrib.admin.views.decorators import  staff_member_required
from .models import Orden
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
#import weasyprint


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Orden, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order':order,})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrdenCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                                        orden=order,
                                        product=item['product'],
                                        precio=item['price'],
                                        cantidad=item['quantity'],
                )
            #limpiamos l carro
            cart.clear()
            #lanzamos el proceso asincrono
            order_created.delay(order.id)
            #set the order in the session
            request.session['order_id'] = order.id
            #redirect to the payment
            return redirect(reverse('payment:process'))

    else:
        form = OrdenCreateForm()
    return render(request, 'orders/order/created.html', {'cart':cart, 'form':form})

#@staff_member_required
#def admin_order_pdf(request, order_id):
    #order = get_object_or_404(Orden, id=order_id)
    #html = render_to_string('orders/order/pdf.html')
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'filename=/"order_{}.pdf"'.format(order.id)
    #weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css./pdf.css')])
    #return response
