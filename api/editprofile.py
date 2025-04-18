# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.utils.html import format_html  # تأكد من استيراد format_html

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=100, blank=True, null=True)  # إضافة حقل الإيميل
  
    def __str__(self):
        return f"{self.user.username} "

    def clean(self):
        if self.profile_picture:
            file_extension = self.profile_picture.name.split('.')[-1].lower()
            if file_extension not in ['jpg', 'jpeg', 'png']:
                raise ValidationError("Profile picture must be a JPG, JPEG, or PNG image.")
        super().clean()

# serializers.py
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'  # يشمل جميع الحقول بما فيها الإيميل

# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])  # تأكد من أن المستخدم مسجل دخول
def edit_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # إضافة حقل الإيميل إلى البيانات القادمة مع الطلب
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except ValidationError as e:
                return Response({"error": f"Profile picture error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# urls.py
from django.urls import path
urlpatterns = [
    path('editprofile/', edit_profile, name='edit_profile'),  # صفحة تعديل الملف الشخصي فقط
]

# admin.py
from django.contrib import admin


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'email', 'view_api_link')  # إضافة العمود الجديد

    def view_api_link(self, obj):
        # إضافة رابط API الخاص بتعديل الملف الشخصي
        url = f'http://localhost:8000/api/editprofile/'
        return format_html(f'<a href="{url}" target="_blank">View API</a>')  # يفتح الرابط في نافذة جديدة
    
    view_api_link.short_description = 'API Link'  # تغيير اسم العمود في الواجهة

# تسجيل النموذج في لوحة الإدارة
admin.site.register(UserProfile, UserProfileAdmin)