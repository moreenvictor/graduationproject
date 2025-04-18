from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from rest_framework.permissions import AllowAny


from rest_framework.decorators import api_view
from rest_framework.response import Response
import pyotp  # مكتبة لتوليد OTP
from twilio.rest import Client  # يمكنك استخدام Twilio لإرسال الرسائل

@api_view(['POST'])
def send_otp(request):
    phone_number = request.data.get('phone_number')
    
    # توليد رمز OTP
    totp = pyotp.TOTP('base32secret3232')  # هذا مفتاحك السري لتوليد الرمز
    otp = totp.now()

    # إرسال OTP عبر Twilio
    client = Client('ACCOUNT_SID', 'AUTH_TOKEN')
    message = client.messages.create(
        body=f"Your OTP code is {otp}",
        from_='+1234567890',  # الرقم الذي سترسل منه الرسالة
        to=phone_number
    )

    return Response({"message": "OTP sent successfully"})


@api_view(['POST'])
def verify_otp(request):
    otp_entered = request.data.get('otp')
    phone_number = request.data.get('phone_number')

    # تحقق من أن OTP المدخل صحيح
    totp = pyotp.TOTP('base32secret3232')  # نفس المفتاح السري المستخدم
    if totp.verify(otp_entered):
        return Response({"message": "OTP verified successfully"})
    return Response({"message": "Invalid OTP"}, status=400)


from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def update_password(request):
    phone_number = request.data.get('phone_number')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if new_password != confirm_password:
        return Response({"message": "Passwords do not match"}, status=400)

    # البحث عن المستخدم بناءً على الرقم المدخل
    try:
        user = User.objects.get(profile__phone_number=phone_number)  # نفترض أن الرقم في موديل الـ Profile
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully"})
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=400)


@api_view(['GET'])
def back_to_signin(request):
    return Response({"message": "Redirecting to sign-in page"})


