from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from rest_framework.permissions import IsAuthenticated

from KreditCart.paginations import CustomPagination
from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(for_sale=True)
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination
    serializer_class = ProductSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination
    serializer_class = StockSerializer
