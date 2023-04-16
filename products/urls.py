from django.urls import path
from . import views 


urlpatterns = [
    path('products/', views.get_products, name='get_products'),
    path("products/create_product/", views.create_new_product, name='create_new_product'),
    path("products/upload_images/", views.upload_product_images, name='upload_product_images'),
    path('products/<str:pk>/', views.get_one_product, name='get_one_product'),
    path('products/<str:pk>/update_product/', views.update_product, name='update_product'),
    path('products/<str:pk>/delete_product/', views.delete_product, name='delete_product'),
]
