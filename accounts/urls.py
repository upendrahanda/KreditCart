from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='account'),

urlpatterns = [
              ] + router.urls
