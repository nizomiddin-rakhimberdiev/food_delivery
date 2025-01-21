from django.contrib import admin
from .models import *
# Register your models here.



class CategoryAdmin(admin.ModelAdmin):
    model = FoodCategory
    list_display = ( 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    

admin.site.register(Restaurant)
admin.site.register(FoodCategory, CategoryAdmin)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
