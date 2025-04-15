from django.urls import path
from django.contrib import admin
from api.editprofile import edit_profile  # استيراد الدالة edit_profile
from api.recyclebag import create_recycle_bag, update_recycle_bag  # استيراد الدوال create_recycle_bag و update_recycle_bag
from api.notifications import home_notify  # استيراد الدالة home_notify

urlpatterns = [
    # مسارات API
    path('api/edit-profile/', edit_profile, name='edit_profile'),
    path('api/create-recycle-bag/', create_recycle_bag, name='create_recycle_bag'),
    path('api/update-recycle-bag/', update_recycle_bag, name='update_recycle_bag'),
   
    # مسارات إضافية للإشعارات
    path('api/home/notify/', home_notify, name='home_notify'),
    
    # لوحة تحكم الأدمن
    path('admin/', admin.site.urls),
]
