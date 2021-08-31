from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (
    ProductsView,
    ProductView,
    DishesView,
    DishView,
    CustomRegistration,
    CustomLogin,
    CustomRefresh,
    CustomLogout,
)


urls = [
    path(r"products", ProductsView.as_view()),
    path(r"products/<int:product_id>", ProductView.as_view()),
    path(r"dishes", DishesView.as_view()),
    path(r"dishes/<int:dish_id>", DishView.as_view()),
    path(r"register", CustomRegistration.as_view()),
    path(r"login", CustomLogin.as_view()),
    path(r"logout", CustomLogout.as_view()),
    path(r"token/refresh", CustomRefresh.as_view()),
    path(r"token/verify", TokenVerifyView.as_view()),
]
