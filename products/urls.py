from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, StockViewSet

router = DefaultRouter()

router.register(r'product', ProductViewSet, basename='product')
router.register(r'stock', StockViewSet, basename='stock')

urlpatterns = [
              ] + router.urls
