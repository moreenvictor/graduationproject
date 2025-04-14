from django.urls import path
from .views import NotificationsView, RecycleBagView, EditProfileView, RecycleView, MarkNotificationAsRead, ItemList
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    path('recycle-bag/', RecycleBagView.as_view(), name='recycle_bag'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('recycle/', RecycleView.as_view(), name='recycle'),
    path('items/', ItemList.as_view(), name='items'),
    path('notifications/<int:pk>/read/', MarkNotificationAsRead.as_view(), name='mark_notification_as_read'),  # المسار هنا
    path('login/', TokenObtainPairView.as_view(), name='login'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


