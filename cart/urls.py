from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cart_detail, name='cart_detail'),
    url(r'^add/(?P<product_id>\d+)/$',views.cart_add,name='cart_add'),
    url(r'^remove/(?P<product_id>\d+)/$',views.cart_remove,name='cart_remove'),


    #comparar
    url(r'^comparar/', views.ccart_detail, name='ccart_detail'),
    url(r'^cadd/(?P<product_id>\d+)/$',views.ccart_add,name='ccart_add'),
    url(r'^cremove/(?P<product_id>\d+)/$',views.ccart_remove,name='ccart_remove'),
]