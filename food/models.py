from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from enum import Enum
from copy import deepcopy
from datetime import date


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Measure(Enum):
    KILOGRAM = 1
    PIECE = 2
    LITRE = 3

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True, blank=False)
    quantity = models.PositiveSmallIntegerField(default=0, blank=False)
    date_modified = models.DateField(auto_now_add=True)
    measure = models.IntegerField(choices=Measure.choices())
    category = models.CharField(max_length=30)

    def to_dict(self) -> dict:
        properties = deepcopy(vars(self))
        del properties["_state"]
        return properties

    def save(self, *args, **kwargs):
        self.date_modified = date.today()
        super(Product, self).save()


class Dish(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, blank=False)
    photo = models.TextField()
    recipe = models.TextField(blank=False)
    date_modified = models.DateField(auto_now_add=True)

    def insert_products(self, products: dict):
        """
        :param products: dictionary, contains product_name and quantity of product
        Example: {"tomato": 1}
        """
        for key, value in products.items():
            p = Product.objects.get(name=key)
            DishProduct(dish=self, product=p, quantity=value)

    def get_products(self) -> dict:
        products_dishes = self.dishesproducts_set.all()
        data = {}
        for pd in products_dishes:
            data[pd.product.name] = pd.quantity
        return data

    def to_dict(self) -> dict:
        properties = deepcopy(vars(self))
        del properties["_state"]
        return properties

    def save(self, *args, **kwargs):
        self.date_modified = date.today()
        super(Dish, self).save()


class DishProduct(models.Model):
    id = models.AutoField(primary_key=True)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=False)
