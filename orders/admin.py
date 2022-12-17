from django.contrib import admin

# Register your models here.
from orders.models import OrderLock, Order, OrderDetail

admin.site.register(OrderLock)
admin.site.register(Order)
admin.site.register(OrderDetail)