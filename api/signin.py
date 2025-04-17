from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
