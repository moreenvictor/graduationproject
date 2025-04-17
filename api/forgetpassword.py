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
def forget_password(request):
    email = request.data.get('email')
    new_password = request.data.get('new_password')

    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)