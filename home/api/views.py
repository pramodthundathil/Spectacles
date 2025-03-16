from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from merchant.models import Products
from ..serializer import ProductSerializer, ProductSerializer_without_image
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import viewsets, status


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['id'] = user.id  # This should match 'id'
        token['first_name'] = user.first_name
        return token

    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def demo_data(request):
    data = {
        "product_name":"Test name",
        "product_price":1200,
        "category":"MEN"
    }

    return Response(data)


@api_view(['GET'])
def product_list(request):
    product = Products.objects.all()

    serializer = ProductSerializer(product, many = True)

    return Response(serializer.data)


@api_view(['GET'])
def product_single(request,pk):
    product = get_object_or_404(Products, id = pk)

    serializer = ProductSerializer(instance = product)

    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def product_single_with_id(request):

    pk = request.data.get("id")
    product = get_object_or_404(Products, id = pk)

    serializer = ProductSerializer(instance = product)

    return Response(serializer.data)


@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer_without_image(data = request.data)
    if serializer.is_valid():
        product = serializer.save()
        product.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)

@api_view(['POST'])
def delete_product(request):
    pk = request.data.get('id')
    product = get_object_or_404(Products, id = int(pk))
    product.delete()
    return Response({"Message":"Product Deleted....."})



class ProductViewset(viewsets.ModelViewSet):

    queryset = Products.objects.all()

    serializer_class = ProductSerializer_without_image

    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        # Custom response for successful creation
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "message": "Category created successfully!",
                "data": response.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        # Custom response for successful update
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "message": "Category updated successfully!",
                "data": response.data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        # Custom response for successful deletion
        super().destroy(request, *args, **kwargs)
        return Response(
            {
                "message": "Category deleted successfully!",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
