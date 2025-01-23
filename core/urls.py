from django.urls import path

from core import views
from core.views import home_view, restaurant_view, CartView, AddToCartView, UpdateCartItemView, RemoveFromCartView, \
    ClearCartView

urlpatterns = [
    path('', home_view, name='home'),
    path('restaurants/<int:id>/', restaurant_view, name='restaurant'),
    path('contact/', views.contact_view, name='contact'),
    path('shopping-cart/', views.shoping_cart, name='shopping-cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # path('cart/', views.cart_view, name='cart_view'),  # Bu 'cart_view' URL nomi
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # path('cart/', views.cart_view, name='cart_view'),

    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:food_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update/<int:item_id>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/clear/', ClearCartView.as_view(), name='clear_cart'),
]
