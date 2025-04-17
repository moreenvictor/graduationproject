# models.py
from django.db import models
from django.contrib.auth.models import User

# موديل الإشعار
class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.title}"


# serializers.py
from rest_framework import serializers


# Serializer للإشعار
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from firebase_admin import messaging

# دالة لإرسال الإشعار
def send_push_notification(user, title, message):
    # إرسال إشعار FCM
    try:
       
        user_profile = user.userprofile  
        fcm_token = user_profile.fcm_token  

        if fcm_token:
            # إعداد إشعار FCM
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=message,
                ),
                token=fcm_token,
            )
            # إرسال الإشعار
            response = messaging.send(message)
            print("Successfully sent message:", response)
        else:
            print("FCM token not found for user:", user.username)
    except Exception as e:
        print(f"Error sending push notification: {e}")


# دالة لعرض الإشعارات
@api_view(['GET'])
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-date_created')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


# دالة لإرسال إشعار للمستخدم
@api_view(['POST'])
def create_notification(request):
    title = request.data.get('title')
    message = request.data.get('message')
    user = request.user  # افترضنا أنك تستخدم نظام تسجيل الدخول

    if not title or not message:
        return Response({"error": "Title and message are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    notification = Notification.objects.create(
        title=title,
        message=message,
        user=user
    )

    # إرسال إشعار FCM
    send_push_notification(user, title, message)

    # إرجاع الإشعار الذي تم إنشاؤه
    serializer = NotificationSerializer(notification)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
# في ملف api/notifications.py
from django.http import JsonResponse

def home_notify(request):
    return JsonResponse({'message': 'Notification sent!'})


# urls.py
from django.urls import path


urlpatterns = [
    path('notifications/', get_notifications, name='get_notifications'),
    path('notifications/create/', create_notification, name='create_notification'),
]


# admin.py
from django.contrib import admin

admin.site.register(Notification)

from . import notifications
urlpatterns = [
    path('notifications/', notifications.get_notifications, name='notifications'),]






