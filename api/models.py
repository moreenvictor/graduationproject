from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 

class Material(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    fcm_token = models.CharField(max_length=255, null=True, blank=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class RecycleBag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.material.name} - {self.points} points"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class RecycledItem(models.Model):
    name = models.CharField(max_length=255)
    material = models.CharField(max_length=100)
    weight = models.FloatField()
    date_recycled = models.DateTimeField(default=timezone.now)  # إضافة القيمة الافتراضية هنا

    def __str__(self):
        return f"{self.name} ({self.material})"