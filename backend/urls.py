from django.urls import path
from django.contrib import admin
from api.recyclebags import get_recycle_bags, create_recycle_bag, update_recycle_bag, confirm_order
from api import editprofile
from api import notifications
from api import signin
from api.signup import sign_up

urlpatterns = [

    path('admin/', admin.site.urls),

    # auth
    path('api/signup/', sign_up, name='sign_up'),
    path('api/signin/', signin.SignInView.as_view(), name='sign_in'),

    # profile
    path('api/editprofile/', editprofile.edit_profile, name='edit_profile'),

    # recyclebags
    path('api/recyclebags/', get_recycle_bags, name='get_recycle_bags'),
    path('api/recyclebags/create/', create_recycle_bag, name='create_recycle_bag'),
    path('api/recyclebags/update/<int:pk>/', update_recycle_bag, name='update_recycle_bag'),
    path('orders/confirm/<int:pk>/', confirm_order, name='confirm_order'),

    # notifications
    path('api/notifications/', notifications.get_notifications, name='get_notifications'),
    path('api/notifications/create/', notifications.create_notification, name='create_notification'),
]


  

