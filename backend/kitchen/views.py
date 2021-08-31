from django.shortcuts import render


def index(request):
    return render(request, "index.html", {})


def register(request):
    return render(request, "register.html", {})


def login(request):
    return render(request, "login.html", {})


def dishes(request):
    return render(request, "dishes.html", {})


def dish_detail(request, dish_id):
    return render(request, "detail_dish.html", {})


def products(request):
    return render(request, "products.html", {})
