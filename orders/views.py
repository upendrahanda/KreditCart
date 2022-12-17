import datetime
import json
import time

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from KreditCart.paginations import CustomPagination
from products.models import Stock, Product
from .models import Order, OrderLock, OrderDetail
from .serializers import OrderSerializer


def lock_status(order_lock, itr):
    if order_lock is None:
        order_lock = OrderLock(lock=False)
        order_lock.save()
    if order_lock.lock:
        itr += 1
        if itr > 5:  # five trials
            return False
        time.sleep(1)  # each trial of 1 second
        lock_status(order_lock, itr)
    else:
        order_lock.lock = True
        order_lock.save()
        return True


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Order.objects.all()
        if self.request.GET.get('username'):  # for checking order history by username
            queryset = queryset.filter(user__username=self.request.GET.get('username'))
        return queryset

    def create(self, request):  # overriding for various validations
        data = request.data
        order_lock = OrderLock.objects.all().first()
        status_lock = lock_status(order_lock, 0)
        try:
            if not status_lock:
                return Response({"error": "Your order could not be processed at "
                                          "this time due to high congestion. Please try again later"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            for sku, quantity in data.get('items').items():
                stock = Stock.objects.get(product__sku=sku)
                product_name = stock.product.name
                product_quantity = stock.quantity
                if product_quantity < quantity:
                    order_lock.lock = False
                    order_lock.save()
                    return Response({"error": "Requested quantity {0} for the product {1} is not available. Only {2} "
                                              "left".format(quantity, product_name, product_quantity)},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    data = request.data
                    order_id = str(datetime.datetime.utcnow())
                    order_id = order_id.replace(":", "")
                    order_id = order_id.replace("-", "")
                    order_id = order_id.replace(" ", "")
                    order_id = order_id.replace(".", "")
                    data["order_id"] = order_id
                    payable_amount = 0
                    net_discount = 0
                    with transaction.atomic():
                        try:
                            data["payment_amount"] = 0
                            data["taxes"] = 0
                            data["bill_amount"] = 0
                            data["net_discount"] = 0
                            data["user"] = request.user.user_id

                            serializer = self.get_serializer(data=data)
                            serializer.is_valid(raise_exception=True)
                            resp = serializer.save()

                            for sku, quantity in data.get('items').items():
                                stock = Stock.objects.get(product__sku=sku)
                                product = Product.objects.get(sku=sku)
                                discount = product.price * 0.10  # assuming 10% discount, but can implement dynamic
                                # discounts or coupon based even
                                order_detail = OrderDetail(order_id=resp.id, product_id=product.id, quantity=quantity, discount=discount)
                                payable_amount += product.price - discount
                                net_discount += discount
                                stock.quantity -= quantity
                                stock.save()
                                order_detail.save()

                            data["payment_amount"] = payable_amount
                            taxes = payable_amount*0.18
                            data["taxes"] = taxes  # assuming, but we can implement dynamic tax-slabs
                            data["bill_amount"] = payable_amount + taxes
                            data["net_discount"] = net_discount
                            data["user"] = request.user.user_id

                            serializer = self.get_serializer(resp, data=data)
                            serializer.is_valid(raise_exception=True)
                            serializer.save()

                            order_lock.lock = False
                            order_lock.save()
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        except Exception as e:
                            order_lock.lock = False
                            order_lock.save()
                            print(e)
                            return Response(
                                {"error": "Some internal error occurred"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:  # revoke the lock if error occurs
            print(e)
            order_lock.lock = False
            order_lock.save()
            return Response(
                {"error": "Some internal error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
