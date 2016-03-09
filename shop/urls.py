from django.conf.urls import url
from . import views
from django.conf import settings
from  django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.producto_lista, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$',views.producto_lista, name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.producto_detalle,name='producto_detalle'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)