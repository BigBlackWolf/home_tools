from django.contrib import admin
from .models import Dish, Product, CustomUser
from django.contrib.auth.admin import UserAdmin


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Dish)
admin.site.register(Product)
