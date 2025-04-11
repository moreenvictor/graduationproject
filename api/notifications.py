# notifications.py
from pyfcm import FCMNotification
from django.conf import settings

push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)

def send_notification(user, title, message):
    token = user.userprofile.fcm_token
    if token:  # التأكد من وجود fcm_token
        result = push_service.notify_single_device(
            registration_id=token,
            message_title=title,
            message_body=message
        )
        return result
    return None
