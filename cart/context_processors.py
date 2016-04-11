from .cart import Cart
from .comparate import Comparar

def cart(request):
    return {'cart':Cart(request)}

def comparar(request):
    return {'comparar':Comparar(request)}