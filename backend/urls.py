from django.urls import path
from django.contrib import admin
from api.editprofile import edit_profile  # استيراد الدالة edit_profile
from api.recyclebag import create_recycle_bag, update_recycle_bag  # استيراد الدوال create_recycle_bag و update_recycle_bag
from api.notifications import home_notify  # استيراد الدالة home_notify
from api import editprofile
urlpatterns = [
    # مسارات API
    path('api/edit-profile/', edit_profile, name='edit_profile'),
    path('api/create-recycle-bag/', create_recycle_bag, name='create_recycle_bag'),
    path('api/update-recycle-bag/', update_recycle_bag, name='update_recycle_bag'),
   
    # مسارات إضافية للإشعارات
    path('api/home/notify/', home_notify, name='home_notify'),
    path('admin/', admin.site.urls),
    path('api/editprofile/', editprofile.edit_profile, name='edit_profile'),
    path('api/signup/', editprofile.sign_up, name='sign_up'),
    path('api/signin/', editprofile.sign_in, name='sign_in'),
    path('api/forgetpassword/', editprofile.forget_password, name='forget_password'),
]
