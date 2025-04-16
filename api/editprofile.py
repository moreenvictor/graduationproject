# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    CUSTOMER = 'Customer'
    DELIVERY_BOY = 'Delivery Boy'

    USER_TYPE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (DELIVERY_BOY, 'Delivery Boy'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=CUSTOMER)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# serializers.py
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

@api_view(['GET', 'PUT'])
def edit_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # إ تحديث البيانات
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# urls.py
from django.urls import path 
urlpatterns = [
    path('editprofile/', edit_profile, name='edit_profile'),
]

# admin.py
from django.contrib import admin

admin.site.register(UserProfile)


