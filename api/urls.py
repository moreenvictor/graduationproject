# api/urls.py
from django.urls import path
from . import editprofile, notifications
from api.recyclebag import create_recycle_bag 
urlpatterns = [
    path('editprofile/', editprofile.edit_profile, name='edit_profile'),
    path('recyclebag/', create_recycle_bag, name='recycle_bag'),   
    path('notifications/', notifications.get_notifications, name='notifications'),
]
