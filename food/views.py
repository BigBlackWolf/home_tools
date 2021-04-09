from rest_framework.views import APIView
from rest_framework.response import Response


class Main(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"response": 1})

    def post(self, request, *args, **kwargs):
        data = request.data
