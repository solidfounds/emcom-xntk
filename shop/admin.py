from django.contrib import admin

# Register your models here.
from .models import Producto, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug']
    prepopulated_fields = { 'slug':('nombre',)}

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'precio', 'stock', 'disponible', 'creado', 'actualizado']
    list_filter = ['disponible', 'creado', 'actualizado']
    list_editable = ['precio', 'stock', 'disponible']
    prepopulated_fields = {'slug':('nombre',)}

