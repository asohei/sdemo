from django.urls import path
from . import views

urlpatterns = [
    path('checkout', views.checkout, name='checkout'),
    path('create_checkout_session', views.create_checkout_session, name='create_checkout_session'),
    path('create_payment', views.create_payment, name='create_payment'),
    path('charge_token', views.charge_token, name='charge_token'),
    path('custom', views.custom, name='custom'),
    path('custom5', views.custom5, name='custom5'),
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
