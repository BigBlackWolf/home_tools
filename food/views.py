from rest_framework.views import APIView
from rest_framework.response import Response
from marshmallow.exceptions import ValidationError
from django.db.utils import IntegrityError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import Product, Dish, CustomUser
from .validations import (
    ProductValidator,
    DishValidator,
    LoginValidator,
    RegistrationValidation,
)


def handle_validation(func, *args, **kwargs):
    def lower(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return Response({"data": e.messages}, status=422)
        except IntegrityError as e:
            return Response({"error": e.args[1]}, status=422)
    return lower


class CustomGetToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        schema = LoginValidator()
        user = schema.load(request.data.get("data", {}))
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username})


class CustomRegistration(APIView):
    def post(self, request, *args, **kwargs):
        schema = RegistrationValidation()
        validated = schema.load(request.data.get("data", {}))
        user = CustomUser(**validated)
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"username": user.username, "token": token.key})


class ProductsView(APIView):
    def get(self, request, *args, **kwargs):
        result = Product.objects.all().values()
        return Response({"data": result})

    @handle_validation
    def post(self, request, *args, **kwargs):
        user_data = request.data.get("data", {})
        data = []
        schema = ProductValidator()
        validated = schema.load(user_data)
        db_obj = Product(**validated)
        db_obj.save()
        obj = db_obj.to_dict()
        data.append(obj)
        return Response({"data": data})


class ProductView(APIView):
    def get(self, request, product_id, *args, **kwargs):
        data = Product.objects.filter(id=product_id).values()
        result = next(iter(data), {})
        return Response({"data": result})

    def patch(self, request, product_id, *args, **kwargs):
        schema = ProductValidator()
        validated = schema.load(request.data.get("data", {}))

        product = Product.objects.filter(id=product_id)
        product.update(**validated)
        data = product.values()
        result = next(iter(data), {})
        return Response({"data": result})

    def delete(self, request, product_id, *args, **kwargs):
        Product.objects.filter(id=product_id).delete()
        return Response({"data": "Success"})


class DishesView(APIView):
    def get(self, request, *args, **kwargs):
        result = Dish.objects.all().values()
        return Response({"data": result})

    @handle_validation
    def post(self, request, *args, **kwargs):
        user_data = request.data.get("data", {})
        data = []
        schema = DishValidator()
        validated = schema.load(user_data)
        ingredients = validated.pop("ingredients", {})
        db_obj = Dish(**validated)
        db_obj.insert_products(ingredients)
        db_obj.save()
        obj = db_obj.to_dict()
        data.append(obj)
        return Response({"data": data})


class DishView(APIView):
    def get(self, request, dish_id, *args, **kwargs):
        data = Dish.objects.filter(id=dish_id).values()
        result = next(iter(data), {})
        return Response({"data": result})

    def patch(self, request, dish_id, *args, **kwargs):
        schema = DishValidator()
        validated = schema.load(request.data.get("data", {}))

        dish = Dish.objects.filter(id=dish_id)
        dish.update(**validated)
        data = dish.values()
        result = next(iter(data), {})
        return Response({"data": result})

    def delete(self, request, dish_id, *args, **kwargs):
        Dish.objects.filter(id=dish_id).delete()
        return Response({"data": "Success"})
