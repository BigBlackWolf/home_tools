from rest_framework.views import APIView
from rest_framework.response import Response
from marshmallow.exceptions import ValidationError
from django.db.utils import IntegrityError

from .models import Products
from .validations import ProductValidator


class Main(APIView):
    def get(self, request, *args, **kwargs):
        result = Products.objects.all().values()
        return Response({"products": result})

    def post(self, request, *args, **kwargs):
        user_data = request.data
        data = []
        try:
            for i in user_data["products"]:
                schema = ProductValidator()
                validated = schema.load(i)
                db_obj = Products(**validated)
                db_obj.save()
                data.append(validated)
        except ValidationError as e:
            data = e.messages
        except IntegrityError as e:
            data = {"error": e.args[1]}
        return Response({"data": data})
