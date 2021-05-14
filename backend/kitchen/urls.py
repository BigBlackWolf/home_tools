from django.urls import path
from .views import dishes, products, index, register, login

urls = [
    path(r"dishes/", dishes),
    path(r"products/", products),
    path(r"", index),
    path(r"register/", register),
    path(r"login/", login),
    # path(r"products/", ProductsView.as_view()),
    # path(r"products/<int:product_id>", ProductView.as_view()),
    # path(r"dishes/<int:dish_id>", DishView.as_view()),
    # path(r"register/", CustomRegistration.as_view()),
    # path(r"login/", CustomLogin.as_view()),
    # path(r"logout/", CustomLogout.as_view()),
]
