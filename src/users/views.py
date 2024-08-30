from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from users.serializers import UserRegisterSerializer


class UserRegistration(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        User registration.
        """
        data = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password": request.data.get("password"),
            "password2": request.data.get("password2"),
        }
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "User was created"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
