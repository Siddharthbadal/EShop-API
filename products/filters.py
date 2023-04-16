from django_filters import rest_framework as filters
from .models import Products


class ProductFilter(filters.FilterSet):

    keyword = filters.CharFilter(field_name="description", lookup_expr="icontains")
    min_price = filters.NumberFilter(field_name="price" or 0, lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")


    class Meta:
        model = Products
        fields = ('keyword', 'category', 'brand', 'ratings', 'min_price', 'max_price')
    
    