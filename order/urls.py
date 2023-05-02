from django.urls import path 
from . import views 

urlpatterns = [
    path('orders/new/', views.new_order, name='new_order'),
    path('orders/', views.get_all_orders, name='get_all_orders'),
    path('orders/<str:pk>/', views.get_one_order, name='get_one_order'),
    path('orders/<str:pk>/update', views.process_order, name='process_order'),
    path('orders/<str:pk>/delete', views.delete_order, name='delete_order'),
]
