from django.urls import path
from .views import Main


urls = [
    path(r'', Main.as_view()),
]
