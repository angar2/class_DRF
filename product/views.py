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
        
        product_serializer.is_valid(raise_exception=True) # raise_exception=True: not valid일 경우 error를 띄움
        product_serializer.save()
        return Response(product_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, product_id):
        product = ProductModel.objects.get(id=product_id)
        product_serializer = ProductSerializer(product, data=request.data, partial=True)

        if product_serializer.is_valid(raise_exception=True):
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)

        return Response(product_serializer.error, status=status.HTTP_400_BAD_REQUEST)

        
        
        return Response()
    
    def delete(self, request):
        return Response()