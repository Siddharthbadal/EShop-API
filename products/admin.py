from django.contrib import admin
from .models import Products, ProductImages, Review, Category



@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display =['name', 'brand', 'category', 'stock']

@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['product']



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=['product', 'rating', 'created_at']