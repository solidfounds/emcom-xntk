__author__ = 'seader'
from decimal import  Decimal
from django.conf import settings
from shop.models import Producto
from coupons.models import Coupon

class Comparar(object):

    def __init__(self, request):
        """
        Initialize the comparar.
        """
        self.session = request.session
        comparar = self.session.get(settings.CART_SESSION_IDC)
        if not comparar:
            # save an empty comparar in the session
            comparar = self.session[settings.CART_SESSION_IDC] = {}
        self.comparar = comparar
        self.coupon_id = self.session.get('coupon_id')

    def __len__(self):
        """
        Count all items in the comparar.
        """
        return sum(item['quantity'] for item in self.comparar.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.comparar.keys()
        # get the product objects and add them to the comparar
        products = Producto.objects.filter(id__in=product_ids)
        for product in products:
            self.comparar[str(product.id)]['product'] = product

        for item in self.comparar.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the comparar or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.comparar:
            self.comparar[product_id] = {'quantity': 0,
                                      'price': str(product.precio)}
        if update_quantity:
            self.comparar[product_id]['quantity'] = quantity
        else:
            self.comparar[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        Remove a product from the comparar.
        """
        product_id = str(product.id)
        if product_id in self.comparar:
            del self.comparar[product_id]
            self.save()

    def save(self):
        # update the session comparar
        self.session[settings.CART_SESSION_IDC] = self.comparar
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def clear(self):
        # empty comparar
        self.session[settings.CART_SESSION_IDC] = {}
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.comparar.values())

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()