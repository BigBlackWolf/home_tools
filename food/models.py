from django.db import models
from django.db.utils import IntegrityError
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

from enum import Enum
from datetime import date


class Measure(Enum):
    KILOGRAM = 1
    PIECE = 2
    LITRE = 3

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False)
    quantity = models.PositiveSmallIntegerField(default=0, blank=False)
    date_modified = models.DateField(auto_now_add=True)
    measure = models.IntegerField(choices=Measure.choices())
    category = models.CharField(max_length=30)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def validate_unique(self, exclude=None):
        if Product.objects.filter(name=self.name, user=self.user).exists():
            raise IntegrityError(1062, "Dublicate product")
        super().validate_unique()

    def save(self, *args, **kwargs):
        self.date_modified = date.today()
        self.validate_unique()
        super(Product, self).save()


class Dish(models.Model):
    name = models.CharField(max_length=200, blank=False)
    photo = models.TextField()
    recipe = models.TextField(blank=False)
    date_modified = models.DateField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ingredients = models.JSONField(default=dict)

    def validate_unique(self, exclude=None):
        if Dish.objects.filter(name=self.name, user=self.user).exists():
            raise IntegrityError(1062, "Dublicate dish")
        super().validate_unique()

    def save(self, *args, **kwargs):
        self.date_modified = date.today()
        self.validate_unique()
        super(Dish, self).save()
