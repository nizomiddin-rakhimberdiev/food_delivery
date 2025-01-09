from users.models import CustomUser
from rest_framework import serializers
from core.models import Restaurant, FoodCategory, Food, Order, OrderItem, Payment

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'user_id', 'address', 'role', 'is_staff', 'is_active']



# Serializers

# Restaurant Serializer
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'owner', 'name', 'address', 'phone', 'rating', 'created_at']


# FoodCategory Serializer
class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ['id', 'name', 'description']


# Food Serializer
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'restaurant', 'category', 'name', 'description', 'price', 'image', 'is_available']


# OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'food', 'quantity', 'price']


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'restaurant', 'delivery_person', 'total_price', 'status', 'created_at', 'order_items']


# Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'payment_method', 'is_paid', 'paid_at']
