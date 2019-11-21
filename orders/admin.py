from django.contrib import admin

from .models import Category, Size, Base, Type, Toppings, Order

admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Base)
admin.site.register(Type)
admin.site.register(Toppings)
admin.site.register(Order)
