from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from products.models import Products
from .serializers import OrderItemSerializer, OrderSerializer
from .filters import OrdersFilters
from rest_framework.pagination import PageNumberPagination


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    user = request.user
    data = request.data 

    order_Items = data['orderItems']
    if order_Items and len(order_Items)== 0:
        return Response({"error":"No order Items. Please add one item."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        total_amount =sum(item['price'] * item['quantity'] for item in order_Items)
        order = Order.objects.create(
            user=user,
            street=data['street'],
            city=data['city'],
            state=data['state'],
            zip_code = data['zip_code'],
            phone= data['phone'],
            country=data['country'],
            total_amount=total_amount
        )

        for i in order_Items:
            product = Products.objects.get(id=i["product"])
            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity=i['quantity'],
                price=i['price']
            )


            # update prodcus stock
            product.stock -= item.quantity
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)            


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_orders(request):
    filterset = OrdersFilters(request.GET, queryset=Order.objects.all().order_by('id'))
    count = filterset.qs.count()
    #pagination
    resPerPage = 1
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage
    queryset = paginator.paginate_queryset(filterset.qs, request)

    
    serializer = OrderSerializer(queryset, many=True)
    return Response({
        'count': count,
        'resultPerPage': resPerPage,
        'orders': serializer.data
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_one_order(request, pk):
    orders = get_object_or_404(Order, id=pk)
    serializer = OrderSerializer(orders, many=False)
    return Response({'orders': serializer.data})




@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def process_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.order_status = request.data['order_status']
    serializer = OrderSerializer(order, many=False)

    return Response({'orders': serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_order(request, pk):

    order = get_object_or_404(Order, id=pk)
    order.delete()
    
    

    return Response({'details':'Order deleted'})