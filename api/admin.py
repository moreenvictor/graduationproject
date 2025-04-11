from django.contrib import admin
from .models import Material, UserProfile, RecycleBag, Notification

admin.site.register(Material)
admin.site.register(UserProfile)
admin.site.register(RecycleBag)
admin.site.register(Notification)
