from django.shortcuts import render, redirect

from core.models import FoodCategory, Restaurant, Food, RestaurantBranch, Product

from decimal import Decimal


def home_view(request, *args, **kwargs):
    categories = FoodCategory.objects.all()
    restaurants = Restaurant.objects.all()
    foods = Food.objects.filter(price__isnull=False, discount__isnull=False)

    for food in foods:
        try:
            if food.discount > 0:
                food.price = Decimal(food.price) - Decimal(food.discount)  # Xavfsiz konvertatsiya
        except Exception as e:
            print(f"Error with food {food.name}: {e}")  # Log qoldirish

    context = {
        'categories': categories,
        'restaurants': restaurants,
        'foods': foods,
        'title': 'Home'
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


def abdurahmon_view(request):
    pass




def contact_view(request):
    return render(request, 'contact.html')



# def application_view(request):
#     if request.method == "POST":
#         form = ApplicationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success')  # Ma'lumot saqlangandan keyin boshqa sahifaga o'tish
#     else:
#         form = ApplicationForm()
#     return render(request, 'application_form.html', {'form': form})


def shoping_cart(request):
    return render(request, 'shoping-cart.html')




def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # CartItem yaratishda to'g'ri argumentlardan foydalaning
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)  # product maydoni CartItem modelida bo'lishi kerak
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_view')




def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)  # Foydalanuvchining savatidagi buyurtmalarni olish
    for item in cart_items:
        print(item.product)  # Bu erda product atributi mavjud bo'lishi kerak
    return render(request, 'cart.html', {'cart_items': cart_items})


def shopping_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shopping_cart.html', {'cart': cart})



#
# def set_language(request, lang):
#     # Foydalanuvchi tanlagan tilni faollashtirish
#     activate(lang)
#
#     # Cookie'ni yaratish (tanlangan tilni saqlash)
#     response = redirect(request.META.get('HTTP_REFERER'))  # Foydalanuvchini oldingi sahifaga qaytarish
#     response.set_cookie('django_language', lang)
#
#     return response

@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    """
    Add to Cart View - Oziq-ovqatni savatchaga qo'shish.
    """

    def post(self, request, food_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        food = get_object_or_404(Food, id=food_id)

        # Savatchada mavjud bo'lsa, miqdorni oshirish
        cart_item, created = CartItem.objects.get_or_create(cart=cart, food=food)
        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({
            "message": f"{food.name} savatchaga qo'shildi",
            "quantity": cart_item.quantity
        })


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

