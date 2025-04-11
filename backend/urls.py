from django.contrib import admin
from django.urls import path, include
from api import views  # تأكد من استيراد views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
     # أضف هذا السطر للصفحة الرئيسية
]

from django.urls import path, include
from django.urls import path, include

from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),  # تأكد من أن هذا صحيح
    path('admin/', admin.site.urls),    # مثال لمسار آخر
]


