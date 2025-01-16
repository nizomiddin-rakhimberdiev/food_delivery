from django.shortcuts import render

from core.models import *


# Create your views here.

def home_view(request, *args, **kwargs):
    categories = FoodCategory.objects.all()
    restaurants = Restaurant.objects.all()
    foods = Food.objects.all()
    context = {
        'categories': categories,
        'restaurants': restaurants,
        'title': 'Home'  # Add title to your template in the base.html file, e.g., <title>{{ title }}</title>
    }
    return render(request, 'index.html', context)


def restaurant_view(request, id):
    restaurant = Restaurant.objects.get(id=id)
    restaurants = Restaurant.objects.all()
    context = {
        'restaurant': restaurant,
        'restaurants': restaurants,  # Include all restaurants for navigation bar in the template
        'title': restaurant.name  # Add title to your template in the base.html file, e.g., <title>{{ title }}</title>
    }
    return render(request, 'shop-grid.html', context)

    