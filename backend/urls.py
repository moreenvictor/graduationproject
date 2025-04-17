from django.urls import path
from django.contrib import admin
from api.recyclebags import  get_recycle_bags ,create_recycle_bag, update_recycle_bag   # استيراد الدوال create_recycle_bag و update_recycle_bag
from api.notifications import home_notify  # استيراد الدالة home_notify
from api import editprofile
from api import notifications
urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/editprofile/', editprofile.edit_profile, name='edit_profile'),
    path('api/signup/', editprofile.sign_up, name='sign_up'),
    path('api/signin/', editprofile.sign_in, name='sign_in'),
    path('api/forgetpassword/', editprofile.forget_password, name='forget_password'),
   #reyclebag
    path('api/recyclebags/', get_recycle_bags, name='get_recycle_bags'),
    path('api/recyclebags/create/', create_recycle_bag, name='create_recycle_bag'),
    path('api/recyclebags/update/<int:pk>/', update_recycle_bag, name='update_recycle_bag'),

#notifications
    path('api/notifications/', notifications.get_notifications, name='get_notifications'),
    path('api/notifications/create/', notifications.create_notification, name='create_notification'),
  
]