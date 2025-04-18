from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import random
from twilio.rest import Client
from django.conf import settings
from api.editprofile import UserProfile

# دالة للتحقق من صحة المدخلات
def validate_sign_up_data(email, password, confirm_password, user_type):
    if not email or not password or not confirm_password or not user_type:
        return "Email, password, confirm_password, and user_type are required.", status.HTTP_400_BAD_REQUEST
    
    if user_type not in ['boy', 'customer']:
        return "Invalid user_type. Must be 'boy' or 'customer'.", status.HTTP_400_BAD_REQUEST

    if password != confirm_password:
        return "Password and confirm_password do not match.", status.HTTP_400_BAD_REQUEST

    try:
        validate_email(email)
    except ValidationError:
        return "Invalid email format.", status.HTTP_400_BAD_REQUEST

    if User.objects.filter(email=email).exists():
        return "Email already exists.", status.HTTP_400_BAD_REQUEST

    if len(password) < 8:
        return "Password must be at least 8 characters long.", status.HTTP_400_BAD_REQUEST

    return None, None

# دالة لإنشاء المستخدم
def create_user(email, password):
    user = User.objects.create_user(username=email, email=email, password=password)
    return user

# دالة لإنشاء البروفايل
def create_user_profile(user, first_name, last_name, phone_number, gender, country, birth_date, user_type, profile_picture):
    try:
        profile = UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
            country=country,
            birth_date=birth_date,
            user_type=user_type,
            profile_picture=profile_picture
        )
        return profile
    except Exception as e:
        raise Exception(f"Error creating user profile: {str(e)}")

# دالة لإرسال OTP
def send_otp(phone_number):
    otp = random.randint(100000, 999999)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP code is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return otp

# دالة للتأكد من OTP
def verify_otp_logic(user_otp, sent_otp):
    return user_otp == sent_otp

# دالة تسجيل المستخدم
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    # الحصول على البيانات من الطلب
    email = request.data.get('email')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password') 
    user_type = request.data.get('user_type')  
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    phone_number = request.data.get('phone_number')
    gender = request.data.get('gender')
    country = request.data.get('country')
    birth_date = request.data.get('birth_date')
    profile_picture = request.FILES.get('profile_picture')  # لازم request يكون نوعه multipart/form-data

    # تحقق من المدخلات
    error_message, error_status = validate_sign_up_data(email, password, confirm_password, user_type)
    if error_message:
        return Response({"error": error_message}, status=error_status)

    # إنشاء المستخدم
    user = create_user(email, password)

    # إنشاء بروفايل المستخدم
    try:
        profile = create_user_profile(user, first_name, last_name, phone_number, gender, country, birth_date, user_type, profile_picture)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # إرسال OTP بعد إنشاء المستخدم
    otp = send_otp(phone_number)
    request.session['otp'] = otp  # حفظ OTP في الجلسة

    return Response({"message": "User created successfully. OTP sent to phone."}, status=status.HTTP_201_CREATED)

# دالة للتحقق من OTP
@api_view(['POST'])
def verify_otp(request):
    user_otp = request.data.get("otp")
    sent_otp = request.session.get('otp')

    if verify_otp_logic(user_otp, sent_otp):
        return Response({"message": "OTP verified successfully!"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid OTP, please try again."}, status=status.HTTP_400_BAD_REQUEST)
