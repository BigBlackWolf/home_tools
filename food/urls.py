from django.urls import path
from .views import ProductsView, ProductView, DishesView, DishView


urls = [
    path(r'food/', ProductsView.as_view()),
    path(r'food/<int:product_id>', ProductView.as_view()),
    path(r'dishes/', DishesView.as_view()),
    path(r'dishes/<int:dish_id>', DishView.as_view()),
]
