from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductSerializer
from .models import Product as ProductModel

# Create your views here.
class ProductView(APIView):
    def get(self, request):
        return Response()
    def post(self, request):
        user = request.user
        request.data['author'] = user.id
        product_serializer = ProductSerializer(data = request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response()
    def put(self, request):
        return Response()
    def delete(self, request):
        return Response()