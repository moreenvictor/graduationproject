# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class RecycleBag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material_type = models.CharField(max_length=100)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_collected = models.BooleanField(default=False)
    order_confirmed = models.BooleanField(default=False)
    order_confirmed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Recycle Bag for {self.user.username} - {self.material_type}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recycle_bag = models.ForeignKey(RecycleBag, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    total_count = models.IntegerField()  # عدد المواد في الأوردر
    material_type = models.CharField(max_length=100)  # نوع المادة

    def __str__(self):
        return f"Order for {self.user.username} - {self.material_type}"

# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now

@api_view(['POST'])
def confirm_order(request, pk):
    try:
        recycle_bag = RecycleBag.objects.get(pk=pk, user=request.user)
    except RecycleBag.DoesNotExist:
        return Response({"error": "Recycle Bag not found"}, status=status.HTTP_404_NOT_FOUND)

    # تأكيد الأوردر
    order = Order.objects.create(
        user=request.user,
        recycle_bag=recycle_bag,
        is_confirmed=True,  # تأكيد الأوردر
        confirmed_at=now(),  # تاريخ تأكيد الأوردر
        total_count=recycle_bag.count,  # عدد المواد في الأوردر
        material_type=recycle_bag.material_type  # نوع المادة في الأوردر
    )

    order.save()

    return Response({"message": "Order confirmed successfully", "order_id": order.id}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_recycle_bags(request):
    # استرجاع أكياس التدوير للمستخدم
    recycle_bags = RecycleBag.objects.filter(user=request.user)
    data = [{"id": rb.id, "material_type": rb.material_type, "count": rb.count} for rb in recycle_bags]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_recycle_bag(request):
    # استلام البيانات من الطلب وإنشاء كيس التدوير
    material_type = request.data.get("material_type")
    count = request.data.get("count")
    
    if not material_type or not count:
        return Response({"error": "Material type and count are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    recycle_bag = RecycleBag.objects.create(
        user=request.user,
        material_type=material_type,
        count=count
    )
    
    return Response({"message": "Recycle Bag created successfully", "recycle_bag_id": recycle_bag.id}, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def update_recycle_bag(request, pk):
    try:
        recycle_bag = RecycleBag.objects.get(pk=pk, user=request.user)
    except RecycleBag.DoesNotExist:
        return Response({"error": "Recycle Bag not found"}, status=status.HTTP_404_NOT_FOUND)

    material_type = request.data.get("material_type", recycle_bag.material_type)
    count = request.data.get("count", recycle_bag.count)
    
    recycle_bag.material_type = material_type
    recycle_bag.count = count
    recycle_bag.save()

    return Response({"message": "Recycle Bag updated successfully"}, status=status.HTTP_200_OK)


# urls.py
from django.urls import path

urlpatterns = [
     path('recycle_bags/', get_recycle_bags, name='get_recycle_bags'),
    path('recycle_bags/', get_recycle_bags, name='get_recycle_bags'),
    path('recycle_bags/update/<int:pk>/', update_recycle_bag, name='update_recycle_bag'),
    path('order/confirm/<int:pk>/', confirm_order, name='confirm_order'),
]

# admin.py
from django.contrib import admin


admin.site.register(RecycleBag)
admin.site.register(Order)