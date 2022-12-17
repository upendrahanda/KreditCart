from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from rest_framework.permissions import IsAuthenticated

from KreditCart.paginations import CustomPagination
from .models import CustomUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination
