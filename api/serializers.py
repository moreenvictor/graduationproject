from rest_framework import serializers
from .models import UserProfile, RecycleBag, Material, Notification
from .models import RecycledItem



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class RecycleBagSerializer(serializers.ModelSerializer):
    material = serializers.StringRelatedField()

    class Meta:
        model = RecycleBag
        fields = ['material', 'points']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['title', 'message', 'is_read', 'date_created']

class RecycledItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecycledItem
        fields = ['name', 'material', 'count', 'date_recycled']  # نضيف count بدلاً من weight
