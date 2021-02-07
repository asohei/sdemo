from django.urls import path
from . import views

urlpatterns = [

    path('products', views.products, name='products'),
    path('cart', views.cart, name='cart'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('count_cart_items', views.count_cart_items, name='count_cart_items'),
    path('grab_cart', views.grab_cart, name='grab_cart'),
    path('remove_item', views.remove_item, name='remove_item'),
    path('checkoutstart', views.checkoutstart, name='checkoutstart'),
    path('create_paymentIntent', views.create_paymentIntent, name='create_paymentIntent'),
    path('clear_cart_transaction', views.clear_cart_transaction, name='clear_cart_transaction'),

]
