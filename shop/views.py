from django.shortcuts import render, get_object_or_404

from .models import Producto, Categoria
from cart.forms import CartAddProductForm
from .forms import SearchForm
# Create your views here.

def producto_lista(request, category_slug=None):
    categoria = None
    categorias = Categoria.objects.all()
    productos = Producto.objects.filter(disponible=True)
    if category_slug:
        categoria = get_object_or_404(Categoria, slug=category_slug)
        productos = productos.filter(categoria=categoria)
    return render(request,
                  'shop/producto/list.html',
                  { 'categoria':categoria,
                    'categorias':categorias,
                    'productos':productos

                  })

def producto_detalle(request, id, slug):
    producto = get_object_or_404(Producto,
                                 id=id,
                                 slug=slug,
                                 disponible=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/producto/detalle.html', {'producto':producto,
                                                          'cart_product_form':cart_product_form})

################################################################## buscar
def search_productt(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        products = Producto.objects.filter(nombre__icontains=q)
        context = {'query': q, 'products':products}
        template = 'shop/buscar/results.html'
    else:
        context = {}
        template = 'shop/buscar/buscar.html'
    return render(request, template, context)

################################################################## buscar