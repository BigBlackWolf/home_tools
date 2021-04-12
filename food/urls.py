from django.urls import path
from .views import Main, ProductView


urls = [
    path(r'', Main.as_view()),
    path(r'<int:product_id>', ProductView.as_view()),
]
