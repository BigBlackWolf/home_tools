from django.db import models
from enum import Enum


class Measure(Enum):
    KILOGRAM = 1
    PIECE = 2
    LITRE = 3

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True, blank=False)
    quantity = models.PositiveSmallIntegerField(default=0, blank=False)
    date_modified = models.DateField(auto_now_add=True)
    measure = models.IntegerField(choices=Measure.choices())
    category = models.CharField(max_length=30)


class Dishes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True, blank=False)
    photo = models.TextField()
    recipe = models.TextField(blank=False)
    date_modified = models.DateField(auto_now_add=True)

    def insert_products(self, products: dict):
        """
        :param products: dictionary, contains product_name and quantity of product
        Example: {"tomato": 1}
        """
        for key, value in products.items():
            p = Products.objects.get(name=key)
            DishesProducts(dish=self, product=p, quantity=value)

    def get_products(self) -> dict:
        products_dishes = self.dishesproducts_set.all()
        data = {}
        for pd in products_dishes:
            data[pd.product.name] = pd.quantity
        return data


class DishesProducts(models.Model):
    id = models.AutoField(primary_key=True)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=False)
