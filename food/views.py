from rest_framework.views import APIView
from rest_framework.response import Response
from marshmallow.exceptions import ValidationError
from django.db.utils import IntegrityError

from .models import Products, Dishes
from .validations import ProductValidator, DishValidator


class ProductsView(APIView):
    def get(self, request, *args, **kwargs):
        result = Products.objects.all().values()
        return Response({"data": result})

    def post(self, request, *args, **kwargs):
        user_data = request.data.get("data", {})
        data = []
        schema = ProductValidator()
        try:
            validated = schema.load(user_data)
            db_obj = Products(**validated)
            db_obj.save()
            data.append(validated)
        except ValidationError as e:
            data = e.messages
        except IntegrityError as e:
            data = {"error": e.args[1]}
        return Response({"data": data})


class ProductView(APIView):
    def get(self, request, product_id, *args, **kwargs):
        data = Products.objects.filter(id=product_id).values()
        result = next(iter(data), {})
        return Response({"data": result})

    def patch(self, request, product_id, *args, **kwargs):
        schema = ProductValidator()
        validated = schema.load(request.data.get("data", {}))

        product = Products.objects.filter(id=product_id)
        product.update(**validated)
        return Response({"data": product.values()})

    def delete(self, request, product_id, *args, **kwargs):
        Products.objects.filter(id=product_id).delete()
        return Response({"data": "Success"})


class DishesView(APIView):
    def get(self, request, *args, **kwargs):
        result = Dishes.objects.all().values()
        return Response({"data": result})

    def post(self, request, *args, **kwargs):
        user_data = request.data.get("data", {})
        data = []
        schema = DishValidator()
        try:
            validated = schema.load(user_data)
            ingredients = validated.pop("ingredients", {})

            db_obj = Dishes(**validated)
            db_obj.insert_products(ingredients)
            db_obj.save()
            data.append(validated)
        except ValidationError as e:
            data = e.messages
        except IntegrityError as e:
            data = {"error": e.args[1]}
        return Response({"data": data})


class DishView(APIView):
    def get(self, request, dish_id, *args, **kwargs):
        data = Dishes.objects.filter(id=dish_id).values()
        result = next(iter(data), {})
        return Response({"data": result})

    def patch(self, request, dish_id, *args, **kwargs):
        schema = DishValidator()
        validated = schema.load(request.data.get("data", {}))

        dish = Dishes.objects.filter(id=dish_id)
        dish.update(**validated)
        return Response({"data": dish.values()})

    def delete(self, request, dish_id, *args, **kwargs):
        Dishes.objects.filter(id=dish_id).delete()
        return Response({"data": "Success"})
