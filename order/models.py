from django.db import models
from django.contrib.auth.models import User
from products.models import Products

class PaymentStatus(models.TextChoices):
    PAID = 'PAID'
    UNPAID = 'UNPAID'


class OrderStatus(models.TextChoices):
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'

class PaymentMode(models.TextChoices):
    COD='COD'
    CARD='CARD'
    UPI= 'UPI'



class Order(models.Model):
    street=models.CharField(max_length=150, default='', blank=False)
    city=models.CharField(max_length=150, default='', blank=False)
    state=models.CharField(max_length=150, default='', blank=False)
    zip_code=models.CharField(max_length=150, default='', blank=False)
    phone=models.CharField(max_length=150, default='', blank=False)
    country=models.CharField(max_length=150, default='', blank=False)

    total_amount=models.IntegerField(default=0)
    payment_status = models.CharField(max_length=50, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    order_status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
    payment_mode = models.CharField(choices=PaymentMode.choices, default=PaymentMode.CARD)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='orderitems')
    name = models.CharField(max_length=250, default="", blank=False)
    quantity= models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    image = models.CharField(max_length=500, default='', blank=False)

    def __str__(self):
        return self.name