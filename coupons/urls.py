__author__ = 'mrk2'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^apply/$', views.coupon_apply, name='apply'),
]