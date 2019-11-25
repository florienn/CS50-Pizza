from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model


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
        return f'{self.name}'

class Order(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Toppings, blank=True, related_name='Order')
    user = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
    )

    #price =

    #type.price + toppings.price * quantity

    date_ordered = models.DateTimeField(null=True)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.type}, {self.toppings} for {self.price} by {self.user} is ordered = {self.is_ordered}'
