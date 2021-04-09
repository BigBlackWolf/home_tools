from django.db import models
from enum import Enum


class Products(models.Model):

    class Measure(Enum):
        KILOGRAM = 1
        PIECE = 2
        LITRE = 3

        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)

    name = models.CharField(max_length=30, unique=True)
    quantity = models.IntegerField()
    date_modified = models.DateField()
    measure = models.IntegerField(choices=Measure.choices())
