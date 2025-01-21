from django.shortcuts import render, redirect

from core.models import FoodCategory, Restaurant, Food, RestaurantBranch


# Create your views here.
def home_view(request, *args, **kwargs):
    categories = FoodCategory.objects.all()
    restaurants = Restaurant.objects.all()
    foods = Food.objects.all()
    for food in foods:
        if food.discount > 0:
            food.price -= food.discount
    context = {
        'categories': categories,
        'restaurants': restaurants,
        'foods': foods,  # Include all foods for navigation bar in the template, and display in the shop-grid.html template in the templates folder
        'title': 'Home'  # Add title to your template in the base.html file, e.g., <title>{{ title }}</title>
    }
    return render(request, 'index.html', context)


def restaurant_view(request, id):
    restaurant = Restaurant.objects.get(id=id)
    restaurants = Restaurant.objects.all()
    branches = RestaurantBranch.objects.filter(restaurant=restaurant)
    locations = [
        {"lat": 41.2859051800201, "lng": 69.18616724941523, "name": "Bellissimo Pizza Oazis"},
        {"lat": 41.282554263080314, "lng": 69.20070647808468, "name": "Chorsu Bazaar"},
    ]

    context = {
        'restaurant': restaurant,
        'restaurants': restaurants,  # Include all restaurants for navigation bar in the template
        'branches': branches, # Include all branches for navigation bar in the template
        'locations': locations,  # Add locations for the Google Map in the template
        'title': restaurant.name  # Add title to your template in the base.html file, e.g., <title>{{ title }}</title>
    }
    return render(request, 'shop-grid.html', context)


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Cart, CartItem, Food
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# @method_decorator(login_required, name='dispatch')
class CartView(View):
    """
    Cart View - Savatchani ko'rish yoki yaratish uchun ishlatiladi.
    """

    def get(self, request):
        # Foydalanuvchining savatchasini olish yoki yaratish
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.select_related('food').all()

        # Savatcha ma'lumotlarini JSON formatida qaytarish
        data = {
            "cart_id": cart.id,
            "items": [
                {
                    "id": item.id,
                    "food_name": item.food.name,
                    "quantity": item.quantity,
                    "unit_price": float(item.food.price),
                    "total_price": float(item.total_price())
                }
                for item in cart_items
            ],
            "total_cart_price": sum(item.total_price() for item in cart_items)
        }
        return JsonResponse(data, safe=False)


# @method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    """
    Add to Cart View - Oziq-ovqatni savatchaga qo'shish.
    """

    def get(self, request, food_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        food = get_object_or_404(Food, id=food_id)

        # Savatchada mavjud bo'lsa, miqdorni oshirish
        cart_item, created = CartItem.objects.get_or_create(cart=cart, food=food)
        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return redirect('home')

        # return JsonResponse({
        #     "message": f"{food.name} savatchaga qo'shildi",
        #     "quantity": cart_item.quantity
        # })


@method_decorator(login_required, name='dispatch')
class UpdateCartItemView(View):
    """
    Update Cart Item View - Savatchadagi mahsulot miqdorini yangilash.
    """

    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))  # POST so'rovdan yangi miqdor

        if quantity <= 0:
            cart_item.delete()
            return JsonResponse({"message": "Mahsulot savatchadan olib tashlandi"})

        cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({
            "message": f"{cart_item.food.name} miqdori yangilandi",
            "quantity": cart_item.quantity,
            "total_price": float(cart_item.total_price())
        })


@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(View):
    """
    Remove from Cart View - Mahsulotni savatchadan olib tashlash.
    """

    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()

        return JsonResponse({"message": f"{cart_item.food.name} savatchadan olib tashlandi"})


@method_decorator(login_required, name='dispatch')
class ClearCartView(View):
    """
    Clear Cart View - Savatchani tozalash.
    """

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()

        return JsonResponse({"message": "Savatcha tozalandi"})
