from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Products, ProductImages
from .serializers import ProductsSerializer, ProductImagesSerializer
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


@api_view(['GET'])
def get_products(request):
    """
        View all the products in the store with pagination and filters
    """
    filterset = ProductFilter(request.GET, queryset=Products.objects.all().order_by('id'))

    count = filterset.qs.count()

    resultPerPage = 2
    paginator = PageNumberPagination()
    paginator.page_size =  resultPerPage

    queryset = paginator.paginate_queryset(filterset.qs, request)



    serializer = ProductsSerializer(queryset, many=True)
    return Response({
        "pageCount": count,
        "resultPerPage": resultPerPage,
        "Products": serializer.data
        })


    
@api_view(['GET'])
def get_one_product(request, pk):
    """
        View One product
    """
    product = Products.objects.filter(id=pk)
    #product = get_object_or_404(Products, id=pk)
    serializer = ProductsSerializer(product, many=True)

    return Response({"product": serializer.data})



@api_view(['POST'])
def create_new_product(request):
    """
        create new product    
    """
    data= request.data
    serializer = ProductsSerializer(data=data)

    if serializer.is_valid():
        product = Products.objects.create(**data)
        res = ProductsSerializer(product, many=False)
        return Response({ "product": res.data })
    else:
        return Response(serializer.errors)



@api_view(['POST'])
def upload_product_images(request):
    """
    upload images for a product
    """
    data = request.data
    files = request.FILES.getlist("images")
    print(data)

    images = []
    for f in files:
        image = ProductImages.objects.create(product=Products(data['product']), image=f)
        images.append(image)
        serializer = ProductImagesSerializer(images, many=True)



    return Response(serializer.data)




@api_view(['PUT'])
def update_product(request, pk):
    """
        Update a product's details 
    """
    product = get_object_or_404(Products, id=pk)

    # check if the user is same 
    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.brand = request.data['brand']
    product.category = request.data['category']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']

    product.save()

    serializer = ProductsSerializer(product, many=False)
    return Response({'product': serializer.data})
    

@api_view(['DELETE'])
def delete_product(request, pk):
    """
        Delete a product with images 
    """
    product = get_object_or_404(Products, id=pk)

    args = {"product": pk}
    images = ProductImages.objects.filter(**args)
    for i in images:
        i.delete()

    product.delete()
    return Response({'Details': "Product deleted"}, status=status.HTTP_200_OK)