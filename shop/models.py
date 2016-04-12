from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,db_index=True, unique=True)

    class Meta:
        # ordering = ('nombre',)
        verbose_name = 'Categorias'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                        args=[self.slug])


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='productos')
    nombre = models.CharField(max_length=200, db_index=True)
    marca = models.CharField(max_length=150, default='vacia')
    slug = models.SlugField(max_length=200, db_index=True)
    imagen = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    imagen2 = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    imagen3 = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering = ('nombre')
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('shop:producto_detalle',
                       args=[self.id, self.slug])
