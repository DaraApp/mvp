from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as DjangoUser
from rest_framework.authtoken.models import Token
from user.models import User as CustomUser



class LoginAPI(APIView):
    @staticmethod
    def post(request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate with Django's built-in User model
        user = authenticate(username=username, password=password)

        if user:
            # Get or create token for the user
            token, created = Token.objects.get_or_create(user=user)

            # Try to get the custom user profile
            try:
                custom_user = CustomUser.objects.get(name=user.username)
                user_role = custom_user.role
            except CustomUser.DoesNotExist:
                user_role = "unknown"

            return Response({
                "success": True,
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "role": user_role
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
