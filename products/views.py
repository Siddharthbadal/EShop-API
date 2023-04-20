from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Products, ProductImages, Review
from .serializers import ProductsSerializer, ProductImagesSerializer
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg



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
    # product = get_object_or_404(Products, id=pk)
    print(product)
    serializer = ProductsSerializer(product, many=True)

    return Response({"product": serializer.data})
   



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_new_product(request):
    """
        create new product    
    """
    data= request.data
    serializer = ProductsSerializer(data=data)

    if serializer.is_valid():
        product = Products.objects.create(**data, user=request.user)
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
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    """
        Update a product's details 
    """
    product = get_object_or_404(Products, id=pk)

    # check if the user is same 
    if product.user != request.user:
        return Response({'error':"You are not allowed to update this product"}, status=status.HTTP_403_FORBIDDEN)
    
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
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    """
        Delete a product with images 
    """
    product = get_object_or_404(Products, id=pk)

    if product.user != request.user:
        return Response({'error':"You are not allowed to delete this product!"}, status=status.HTTP_403_FORBIDDEN)
    
    args = {"product": pk}
    images = ProductImages.objects.filter(**args)
    for i in images:
        i.delete()

    product.delete()
    return Response({'Details': "Product deleted"}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, pk):
    user = request.user 
    product = get_object_or_404(Products, id=pk)
    data = request.data

    review = product.reviews.filter(user=user)
    print(type(data['rating']))
    if float(data['rating']) <= 0 or float(data['rating']) > 5:
        return Response({'Error': "Rating is to be between 1 to 5!"}, status=status.HTTP_400_BAD_REQUEST)
    
    elif review.exists():
        new_review  = {
            'rating': data['rating'], 
            'comment': data['comment']
            }
        review.update(**new_review)

        rating = product.reviews.aggregate(avg_rating=Avg('rating'))
        product.ratings =rating['avg_rating']
        product.save()

        return Response({'details': "Review updated"})
    else:
        Review.objects.create(
            user=user,
            product=product,
            rating=data['rating'],
            comment= data['comment']
        )

        rating = product.reviews.aggregate(avg_rating=Avg('rating'))
        product.ratings =rating['avg_rating']
        product.save()
        return Response({'details': "Review posted!"})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):
    user = request.user 
    product = get_object_or_404(Products, id=pk)

    review = product.reviews.filter(user=user)

    if review.exists():
        review.delete()

        rating = product.reviews.aggregate(avg_rating=Avg('rating'))
        
        if rating['avg_rating'] is None:
            rating['avg_rating'] = 0
        
        product.ratings =rating['avg_rating']
        product.save()
        return Response({'details': "Review removed!"})

    else:
        return Response({"error": "Review not found!"}, status=status.HTTP_404_NOT_FOUND)