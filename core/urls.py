

from django.urls import path

from core.views import home_view, restaurant_view

urlpatterns = [
    path('', home_view, name='home'),
    path('restaurants/<int:id>/', restaurant_view, name='restaurant'),
]

