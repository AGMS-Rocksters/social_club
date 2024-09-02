from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import (
    CustomObtainPairSerializer,
    UserRegisterSerializer,
)


class DeleteUserAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        user = request.user

        user.delete()

        return Response(
            {"message": "Your account has been deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class CustomObtainPairView(TokenObtainPairView):
    """
    Obtain JWT token pair using a custom serializer
    that includes the username.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = CustomObtainPairSerializer


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
