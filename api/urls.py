from django.urls import path
from .views import CustomUserListCreateView, CustomUserRetrieveUpdateDestroyView
from django.urls import path
from core.views import (
    RestaurantListCreateView, RestaurantRetrieveUpdateDestroyView,
    FoodCategoryListCreateView, FoodCategoryRetrieveUpdateDestroyView,
    FoodListCreateView, FoodRetrieveUpdateDestroyView,
    OrderListCreateView, OrderRetrieveUpdateDestroyView,
    OrderItemListCreateView, OrderItemRetrieveUpdateDestroyView,
    PaymentListCreateView, PaymentRetrieveUpdateDestroyView,
)
urlpattern = [
    path('users/', CustomUserListCreateView.as_view(), name='customuser-list-create'),
    path('users/<int:pk>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='customuser-detail'),

    path('restaurants/', RestaurantListCreateView.as_view(), name='restaurant-list-create'),
    path('restaurants/<int:pk>/', RestaurantRetrieveUpdateDestroyView.as_view(), name='restaurant-detail'),
    path('categories/', FoodCategoryListCreateView.as_view(), name='foodcategory-list-create'),
    path('categories/<int:pk>/', FoodCategoryRetrieveUpdateDestroyView.as_view(), name='foodcategory-detail'),
    path('foods/', FoodListCreateView.as_view(), name='food-list-create'),
    path('foods/<int:pk>/', FoodRetrieveUpdateDestroyView.as_view(), name='food-detail'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
    path('order-items/', OrderItemListCreateView.as_view(), name='orderitem-list-create'),
    path('order-items/<int:pk>/', OrderItemRetrieveUpdateDestroyView.as_view(), name='orderitem-detail'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentRetrieveUpdateDestroyView.as_view(), name='payment-detail'),
]