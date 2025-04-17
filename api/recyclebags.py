# models.py
from django.db import models
from django.contrib.auth.models import User

# موديل أكياس التدوير
class RecycleBag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material_type = models.CharField(max_length=100)  # نوع المادة مثل بلاستيك، زجاج، إلخ
    count = models.IntegerField(default=0) # عدد الأكياس بدلاً من الوزن
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ الإنشاء
    is_collected = models.BooleanField(default=False)  # هل تم جمع الكيس؟

    def __str__(self):
        return f"Recycle Bag for {self.user.username} - {self.material_type}"


# serializers.py
from rest_framework import serializers

# Serializer لأكياس التدوير
class RecycleBagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecycleBag
        fields = '__all__'  # يتم تضمين الحقول الجديدة تلقائيًا


# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# دالة لإضافة كيس تدوير
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def create_recycle_bag(request):
    # البيانات التي تريد إرسالها
    material_type = request.data.get('material_type')
    count = request.data.get('count')  # استخدم count بدلاً من weight
    user = request.user  # افترضنا أنك تستخدم نظام تسجيل الدخول

    if not material_type or count is None:  # تحقق من الحقل الجديد
        return Response({"error": "Material type and count are required"}, status=status.HTTP_400_BAD_REQUEST)

    # إرسال البيانات إلى API داخلي باستخدام التوكن
    data = {
        "material_type": material_type,  # نوع المادة
        "count": count  # عدد الأكياس
    }

    # الحصول على الـ Token من الـ request أو من مكان آخر
    token = request.headers.get('Authorization')  # إذا كان موجودًا في رأس الطلب

    if not token:
        return JsonResponse({"error": "Token is required for authentication."}, status=401)

    # إضافة الـ Token إلى رأس الطلب
    headers = {
        'Authorization': f'Bearer {token}',
    }

    # رابط الـ API
    url = "http://localhost:8000/api/recyclebags/create/"

    # إرسال طلب POST إلى API الداخلي مع الـ Token
    response = requests.post(url, json=data, headers=headers)

    # التحقق من الاستجابة
    if response.status_code == 201:
        # إنشاء كيس تدوير في النظام
        recycle_bag = RecycleBag.objects.create(
            user=user,
            material_type=material_type,
            count=count,
        )

        # إرجاع الكيس الذي تم إنشاؤه
        serializer = RecycleBagSerializer(recycle_bag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({"error": response.json()}, status=response.status_code)

# دالة لعرض أكياس التدوير الخاصة بالمستخدم
@api_view(['GET'])
def get_recycle_bags(request):
    recycle_bags = RecycleBag.objects.filter(user=request.user).order_by('-created_at')
    serializer = RecycleBagSerializer(recycle_bags, many=True)
    return Response(serializer.data)

# دالة لتحديث حالة جمع كيس التدوير
@api_view(['PATCH'])
def update_recycle_bag(request, pk):
    try:
        recycle_bag = RecycleBag.objects.get(pk=pk, user=request.user)
    except RecycleBag.DoesNotExist:
        return Response({"error": "Recycle Bag not found"}, status=status.HTTP_404_NOT_FOUND)

    is_collected = request.data.get('is_collected', None)

    if is_collected is not None:
        recycle_bag.is_collected = is_collected
        recycle_bag.save()

    # إرجاع الكيس المحدث
    serializer = RecycleBagSerializer(recycle_bag)
    return Response(serializer.data)


# urls.py
from django.urls import path

urlpatterns = [
    path('recycle_bags/', get_recycle_bags, name='get_recycle_bags'),
    path('recycle_bags/create/', create_recycle_bag, name='create_recycle_bag'),
    path('recycle_bags/update/<int:pk>/', update_recycle_bag, name='update_recycle_bag'),
]


# admin.py
from django.contrib import admin

admin.site.register(RecycleBag)







