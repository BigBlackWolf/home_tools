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
