from django.db import models
from shop.models import Producto
# Create your models here.

class Orden(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    email = models.EmailField()
    direccion = models.CharField(max_length=250)
    codigo_postal = models.CharField(max_length=7)
    ciudad = models.CharField(max_length=100)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    pagado = models.BooleanField(default=False)

    class Meta:
        ordering = ('-creado',)

    def __str__(self):
        return 'Orden {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    orden = models.ForeignKey(Orden, related_name='items')
    product = models.ForeignKey(Producto, related_name='order_items')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.precio * self.cantidad