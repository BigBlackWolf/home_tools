import datetime
from django.db.utils import IntegrityError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from marshmallow.exceptions import ValidationError

from .models import Product, Dish, CustomUser
from .validations import (
    ProductValidator,
    DishValidator,
    RegistrationValidation,
)

product_validator = ProductValidator()
dish_validator = DishValidator()
registration_validation = RegistrationValidation()


def handle_errors(func, *args, **kwargs):
    def lower(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return Response({"errors": e.messages}, status=422)
        except IntegrityError as e:
            return Response({"errors": e.args[1]}, status=422)

    return lower


class CustomRefresh(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        data = {"refresh": request.COOKIES.get("refresh", "failed")}
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            response = Response(
                {"errors": e.args[0]}, status=status.HTTP_401_UNAUTHORIZED
            )
            response.delete_cookie("refresh")
            return response
        except AuthenticationFailed as e:
            response = Response(
                {"errors": e.args[0]}, status=status.HTTP_401_UNAUTHORIZED
            )
            response.delete_cookie("refresh")
            return response

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomLogin(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken({"errors": {"credentials": e.args[0]}})
        except AuthenticationFailed as e:
            raise AuthenticationFailed({"errors": {"credentials": e.args[0]}})

        data = serializer.validated_data
        response = Response(data, status=status.HTTP_200_OK)
        expire_date = datetime.datetime.now() + datetime.timedelta(days=1)
        response.set_cookie(
            "refresh", data.get("refresh"), httponly=True, expires=expire_date
        )

        return response


class CustomLogout(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh")
        return response


class CustomRegistration(APIView):
    permission_classes = [AllowAny]

    @handle_errors
    def post(self, request, *args, **kwargs):
        validated = registration_validation.load(request.data)
        user = CustomUser.objects.create_user(**validated)
        user.save()
        return Response({"result": "Success"})


class ProductsView(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(user=request.user).values()
        result = []
        for product in products:
            result.append(product_validator.dump(product))
        return Response({"data": result})

    @handle_errors
    def post(self, request, *args, **kwargs):
        user_data = request.data.get("data", {})
        data = []
        validated = product_validator.load(user_data)
        validated["user"] = request.user
        db_obj = Product(**validated)
        db_obj.save()
        obj = product_validator.dump(db_obj)
        data.append(obj)
        return Response({"data": data})


class ProductView(APIView):
    def get(self, request, product_id, *args, **kwargs):
        data = Product.objects.filter(id=product_id, user=request.user).values()
        result = next(iter(data), {})
        result = product_validator.dump(result)
        return Response({"data": result})

    def patch(self, request, product_id, *args, **kwargs):
        validated = product_validator.load(request.data.get("data", {}))
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
        dishes = Dish.objects.filter(user=request.user).values()
        result = []
        for dish in dishes:
            result.append(dish_validator.dump(dish))
        return Response({"data": result})

    @handle_errors
    def post(self, request, *args, **kwargs):
        user_data = request.data.get("data", {})
        data = []
        validated = dish_validator.load(user_data)
        validated["user"] = request.user
        db_obj = Dish(**validated)
        db_obj.save()
        obj = dish_validator.dump(db_obj)
        data.append(obj)
        return Response({"data": data})


class DishView(APIView):
    def get(self, request, dish_id, *args, **kwargs):
        data = Dish.objects.filter(id=dish_id, user=request.user).values()
        result = next(iter(data), {})
        result = dish_validator.dump(result)
        return Response({"data": result})

    def patch(self, request, dish_id, *args, **kwargs):
        validated = dish_validator.load(request.data.get("data", {}))
        dish = Dish.objects.filter(id=dish_id)
        dish.update(**validated)
        data = dish.values()
        result = next(iter(data), {})
        return Response({"data": result})

    def delete(self, request, dish_id, *args, **kwargs):
        Dish.objects.filter(id=dish_id).delete()
        return Response({"data": "Success"})
