from django.db import models

# Create your models here.
from KreditCart.views import generate_unique_object_id
from accounts.models import CustomUser


class Product(models.Model):
    id = models.CharField(default=generate_unique_object_id, primary_key=True, max_length=24)
    name = models.CharField(max_length=45)
    price = models.PositiveIntegerField()
    sku = models.CharField(max_length=100, unique=True)
    for_sale = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name + self.sku


class Stock(models.Model):
    id = models.CharField(default=generate_unique_object_id, primary_key=True, max_length=24)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'stock'
        verbose_name_plural = 'Stocks'

    def __str__(self):
        return self.product.name + " " + str(self.quantity)


class StockHistory(models.Model):
    id = models.CharField(default=generate_unique_object_id, primary_key=True, max_length=24)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    added_by = models.ForeignKey(CustomUser, limit_choices_to={'groups': 'admin'}, on_delete=models.CASCADE,
                                 related_name='added_by')

    class Meta:
        verbose_name = 'stock_history'
        verbose_name_plural = 'Stock History'

    def __str__(self):
        return self.product.name + " " + str(self.quantity)
