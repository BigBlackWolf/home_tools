from django.urls import path
from .views import dishes, products, index, register, login, dish_detail

urls = [
    path(r"dishes", dishes),
    path(r"dishes/<int:dish_id>", dish_detail),
    path(r"products", products),
    path(r"", index),
    path(r"register", register),
    path(r"login", login),
]
