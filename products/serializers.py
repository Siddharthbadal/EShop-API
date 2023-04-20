from rest_framework import serializers
from .models import Products, ProductImages, Review



class ProductImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields= "__all__"


class ProductsSerializer(serializers.ModelSerializer):
    """
        Product Serializer with fields and fields validations
    """

    images = ProductImagesSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField(method_name='get_reviews', read_only=True)

    class Meta:
        model = Products
        fields = ('id','name', 'description', 'price', 'brand', 'category', 'ratings', 'stock', 'reviews','user', 'created_at', 'images' )

        extra_kwargs = {
            "name": {"required": True, "allow_blank":False},
            "description": {"required": True, "allow_blank":False},
            "category": {"required": True, "allow_blank":False},
            "brand": {"required": True, "allow_blank":False},         

        }

    def get_reviews(self, obj):
        # obj is current product
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields= "__all__"