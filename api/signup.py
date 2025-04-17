from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from editprofile import UserProfile
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    phone_number = request.data.get('phone_number')
    gender = request.data.get('gender')
    country = request.data.get('country')
    birth_date = request.data.get('birth_date')

    if not username or not email or not password:
        return Response({"error": "Username, email, and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_email(email)
    except ValidationError:
        return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    if len(password) < 8:
        return Response({"error": "Password must be at least 8 characters long."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)

    try:
        profile = UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
            country=country,
            birth_date=birth_date
        )
    except Exception as e:
        return Response({"error": f"Error creating user profile: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

