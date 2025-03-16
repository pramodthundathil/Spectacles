from rest_framework.serializers import ModelSerializer 
from merchant.models import Products, ProductImages


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"

class ProductSerializer(ModelSerializer):
    images = ProductImageSerializer( many = True)
    class Meta:
        model = Products
        fields = "__all__"

class ProductSerializer_without_image(ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


