from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return f'{self.name}'

class Size(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return f'{self.name}'

class Base(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return f'{self.name}'

class Type(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default='regular pizza')
    size = models.ForeignKey('Size', on_delete=models.CASCADE, default='none')
    base = models.ForeignKey('Base', on_delete=models.CASCADE, default='none')
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.size} {self.category} with {self.base} for €{self.price}'

class Toppings(models.Model):
    name = models.CharField(max_length=65)
    price = models.DecimalField(max_digits=5, decimal_places=2, default='0.00')

    def __str__(self):
        return f'{self.name} for {self.price} '


class Order(models.Model):
    type = models.CharField(max_length=65, blank=True)
    topping = models.CharField(max_length=65, blank=True)
    topping2 = models.CharField(max_length=65, blank=True)
    topping3 = models.CharField(max_length=65, blank=True)
    quantity = models.IntegerField(default='0')
    user = models.CharField(max_length=65, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default='0.00')
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    is_added = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.type} for {self.price} by {self.user}, ordered = {self.is_ordered} {self.topping} {self.topping2} {self.topping2}'
