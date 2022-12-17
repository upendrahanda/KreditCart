from django.db import models

# Create your models here.
from KreditCart.views import generate_unique_object_id
from accounts.models import CustomUser
from products.models import Product


class Order(models.Model):
    id = models.CharField(default=generate_unique_object_id, primary_key=True, max_length=24)
    order_id = models.CharField(max_length=45)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_amount = models.FloatField()
    net_discount = models.FloatField()
    bill_amount = models.FloatField()
    taxes = models.JSONField(default=dict)
    order_date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'Orders'


class OrderDetail(models.Model):
    id = models.CharField(default=generate_unique_object_id, primary_key=True, max_length=24)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    discount = models.FloatField()

    class Meta:
        verbose_name = 'order_detail'
        verbose_name_plural = 'Order Details'


class OrderLock(models.Model):
    lock = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'order_lock'
        verbose_name_plural = 'Order Lock'
