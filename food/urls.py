from django.urls import path
from .views import ProductsView, ProductView, DishesView, DishView, CustomRegistration
from rest_framework_simplejwt.views import TokenObtainPairView


urls = [
    path(r"products/", ProductsView.as_view()),
    path(r"products/<int:product_id>", ProductView.as_view()),
    path(r"dishes/", DishesView.as_view()),
    path(r"dishes/<int:dish_id>", DishView.as_view()),
    path(r"register/", CustomRegistration.as_view()),
    path(r"login/", TokenObtainPairView.as_view()),
]
