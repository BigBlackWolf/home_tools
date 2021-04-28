from django.urls import path
from .views import ProductsView, ProductView, DishesView, DishView
from .views import CustomGetToken, CustomRegistration


urls = [
    path(r"food/", ProductsView.as_view()),
    path(r"food/<int:product_id>", ProductView.as_view()),
    path(r"dishes/", DishesView.as_view()),
    path(r"dishes/<int:dish_id>", DishView.as_view()),
    path(r"login/", CustomGetToken.as_view()),
    path(r"register/", CustomRegistration.as_view()),
]
