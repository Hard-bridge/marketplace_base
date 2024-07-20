from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('reg', reg),
    path('auth', auth),
    path('panel', panel),
    path('addcart', addcart),
    path('cart', cart),
    path('cartdel', cartdel),
    path('addOrder', addOrder),
    path('payOrder', payOrder),
    path('catalog', catalog),
    path('changecount', changecount),
    path('detail/<int:id_product>', detail),
    path('addreviews',addreviews)
]