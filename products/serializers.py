from rest_framework import serializers
from .models import Product, Stock


class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()

    def get_stock(self, obj):
        try:
            return Stock.objects.get(product_id=obj.id).quantity
        except:
            return -1

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock')


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
