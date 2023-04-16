from rest_framework import serializers
from .models import Products, ProductImages



class ProductImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields= "__all__"


class ProductsSerializer(serializers.ModelSerializer):
    """
        Product Serializer with fields and fields validations
    """

    images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = ('id','name', 'description', 'price', 'brand', 'category', 'ratings', 'stock', 'user', 'created_at', 'images' )

        extra_kwargs = {
            "name": {"required": True, "allow_blank":False},
            "description": {"required": True, "allow_blank":False},
            "category": {"required": True, "allow_blank":False},
            "brand": {"required": True, "allow_blank":False},         

        }


